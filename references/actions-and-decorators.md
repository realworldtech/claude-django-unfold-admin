# Actions and Decorators Reference

## Action Decorator

The `@action` decorator from `unfold.decorators` enhances Django admin actions with additional features.

### Import

```python
from unfold.decorators import action
from unfold.enums import ActionVariant
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `description` | str | Button/link text |
| `permissions` | Iterable[str] | Required permissions |
| `url_path` | str | Custom URL path |
| `icon` | str | Material Symbol name |
| `variant` | ActionVariant | Button style variant |
| `attrs` | dict | Extra HTML attributes (e.g. `{"target": "_blank"}`) |
| `dialog` | dict (`ActionDialog`) | Confirmation/form dialog shown before the action runs |
| `extra_options` | dict | Arbitrary extra options passed through to the action |

The full source signature is:

```python
def action(
    function=None, *, permissions=None, description=None, url_path=None,
    attrs=None, icon=None, variant=ActionVariant.DEFAULT,
    dialog=None, extra_options=None,
):
    ...
```

### ActionVariant Enum

```python
class ActionVariant(Enum):
    DEFAULT = "default"   # Neutral/gray
    PRIMARY = "primary"   # Primary color
    SUCCESS = "success"   # Green
    INFO = "info"         # Blue
    WARNING = "warning"   # Yellow/orange
    DANGER = "danger"     # Red
```

### Action Placement

#### 1. Changelist Actions (actions_list)

Top-level buttons on the changelist page:

```python
class MyModelAdmin(ModelAdmin):
    actions_list = ["export_all", "generate_report"]

    @action(
        description="Export All",
        icon="download",
        variant=ActionVariant.PRIMARY,
    )
    def export_all(self, request):
        # No object_id - operates on all/filtered queryset
        return redirect(...)
```

#### 2. Row Actions (actions_row)

Buttons displayed in each row of the changelist:

```python
class MyModelAdmin(ModelAdmin):
    actions_row = ["quick_edit", "duplicate"]

    @action(
        description="Quick Edit",
        icon="edit",
    )
    def quick_edit(self, request, object_id):
        # object_id is the pk of the row item
        obj = self.get_object(request, object_id)
        return redirect(...)
```

#### 3. Detail Actions (actions_detail)

Buttons at the top of the change form:

```python
class MyModelAdmin(ModelAdmin):
    actions_detail = ["send_email", "archive"]

    @action(
        description="Send Email",
        icon="email",
        permissions=["send_email"],
    )
    def send_email(self, request, object_id):
        obj = self.get_object(request, object_id)
        # Send email logic
        messages.success(request, "Email sent!")
        return redirect(...)

    def has_send_email_permission(self, request, object_id=None):
        return request.user.has_perm("myapp.send_email")
```

#### 4. Submit Line Actions (actions_submit_line)

Buttons in the form submission area:

```python
class MyModelAdmin(ModelAdmin):
    actions_submit_line = ["save_and_notify"]

    @action(description="Save & Notify")
    def save_and_notify(self, request, obj):
        # obj is the model instance (already has pk)
        # Called after form validation, before redirect
        send_notification(obj)
        messages.success(request, "Saved and notification sent!")
```

### Dropdown Groups

Group related actions into a dropdown:

```python
actions_detail = [
    "primary_action",
    {
        "title": "More Actions",
        "items": [
            "action_one",
            "action_two",
            "action_three",
        ],
    },
]
```

### Confirmation & Form Dialogs

Pass `dialog=` to require confirmation — or collect input via a form — before the action runs. When a dialog is set, the handler receives the validated `form` as an extra argument (after `request`).

```python
from django import forms
from unfold.decorators import action
from unfold.forms import BaseDialogForm


class ArchiveForm(BaseDialogForm):
    reason = forms.CharField(label="Reason", required=False)


class MyModelAdmin(ModelAdmin):
    actions_list = ["archive_records"]

    @action(
        description="Archive",
        variant=ActionVariant.WARNING,
        dialog={
            "title": "Archive these records?",
            "description": "This cannot be undone.",
            "form_class": ArchiveForm,        # optional; defaults to BaseDialogForm
            "form_submit_text": "Archive",    # see note below
        },
    )
    def archive_records(self, request, form):
        reason = form.cleaned_data.get("reason")
        # ... do the work ...
        return redirect(...)
```

`ActionDialog` keys (verbatim from source): `title`, `description`, `form_class`, `form_submit_text`.

> **Naming caveat:** the official docs show the submit-button key as `submit_text`, but the actual key in the source is **`form_submit_text`**. Use `form_submit_text`.

**Handler signatures with a dialog** — the validated `form` is inserted right after `request`, on top of the placement's normal signature:

| Placement | With a dialog |
|-----------|---------------|
| `actions_list` | `def my_action(self, request, form)` |
| `actions_row` | `def my_action(self, request, form, object_id)` |
| `actions_detail` | `def my_action(self, request, form, object_id)` |
| `actions_submit_line` | `def my_action(self, request, form, obj)` |

(The example above is an `actions_list` action, hence `(self, request, form)`.)

### Hiding the Default Actions

To suppress Unfold's built-in changelist/change-form actions:

```python
class MyModelAdmin(ModelAdmin):
    actions_list_hide_default = True     # hide default changelist actions
    actions_detail_hide_default = True   # hide default change-form (detail) actions
```

### Permissions

Permissions can be:
1. Method names (without `has_` prefix and `_permission` suffix)
2. Full permission strings (`app.permission_name`)

```python
@action(
    description="Delete",
    permissions=["delete"],  # Calls has_delete_permission
)
def delete_action(self, request, object_id):
    pass

@action(
    description="Export",
    permissions=["myapp.export_data"],  # Checks user.has_perm
)
def export_action(self, request, object_id):
    pass

@action(
    description="Admin Only",
    permissions=["admin_action", "myapp.special_permission"],  # Both must pass
)
def admin_action(self, request, object_id):
    pass
```

For detail/submit_line actions, the permission method receives `object_id`:

```python
def has_publish_permission(self, request, object_id=None):
    if object_id:
        obj = self.get_object(request, object_id)
        return obj.status == "draft" and request.user.has_perm("myapp.publish")
    return request.user.has_perm("myapp.publish")
```

---

## Display Decorator

The `@display` decorator enhances field display in list views.

### Import

```python
from unfold.decorators import display
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `description` | str | Column header text |
| `boolean` | bool | Display as boolean icon (mutually exclusive with `empty_value`) |
| `image` | bool | Display as image |
| `label` | bool/str/dict | Display as label/badge |
| `header` | bool | Display as multi-line header (title/subtitle/initials/avatar) |
| `dropdown` | bool | Display with dropdown content |
| `ordering` | str/expression | Enable sorting |
| `empty_value` | str | Value when empty (mutually exclusive with `boolean`) |
| `wrapper_class` | str | Extra CSS class on the wrapping element |

### Boolean Display

```python
@display(description="Active", boolean=True)
def display_active(self, obj):
    return obj.is_active  # Shows check/x icon
```

### Label Display

Simple label:
```python
@display(description="Status", label=True)
def display_status(self, obj):
    return obj.get_status_display()  # Auto-colored badge
```

Single color for all values:
```python
@display(description="Priority", label="danger")
def display_priority(self, obj):
    return obj.priority  # All red badges
```

Color mapping (valid colors: `success`, `info`, `warning`, `danger`):
```python
@display(
    description="Status",
    label={
        "draft": "warning",     # orange
        "pending": "info",      # blue
        "published": "success", # green
        "archived": "danger",   # red
    }
)
def display_status(self, obj):
    return obj.status
```

### Header Display

A multi-line header cell. The method returns a list of up to **four** elements:

```python
@display(header=True)
def display_user(self, obj):
    return [
        obj.full_name,   # 1: primary text (required)
        obj.email,       # 2: secondary text (or None)
        "AB",            # 3: initials / short text (optional)
        {                # 4: avatar image (optional)
            "path": obj.avatar.url,
            "squared": True,
            "borderless": True,
        },
    ]
```

The two-line form (just title + subtitle) is the common case:
```python
@display(header=True)
def display_user(self, obj):
    return [obj.full_name, obj.email]
```

### Dropdown Display

`dropdown=True` renders an expandable dropdown in the changelist. The method returns a dict. Two shapes are supported.

List of links:
```python
@display(description="Links", dropdown=True)
def display_links(self, obj):
    return {
        "title": "Open",
        "striped": True,   # optional
        "height": 200,     # optional (px)
        "width": 240,      # optional (px)
        "items": [
            {"title": "View on site", "link": obj.get_absolute_url()},
            {"title": "Edit", "link": "#"},
        ],
    }
```

Custom template content:
```python
@display(description="Details", dropdown=True)
def display_details(self, obj):
    return {
        "title": "Click for details",
        "content": f"Full description: {obj.description}",
    }
```

### Image Display

```python
@display(description="Photo", image=True)
def display_photo(self, obj):
    return obj.photo.url if obj.photo else None
```

### Ordering

Enable column sorting:

```python
@display(description="Name", ordering="name")
def display_name(self, obj):
    return obj.name.upper()

# Complex ordering
from django.db.models import F

@display(ordering=F("first_name") + F("last_name"))
def display_full_name(self, obj):
    return f"{obj.first_name} {obj.last_name}"
```

### Empty Value

```python
@display(description="Website", empty_value="No website")
def display_website(self, obj):
    return obj.website
```

### Combined Example

```python
@display(
    description="Author",
    header=True,
    ordering="author__last_name",
)
def display_author(self, obj):
    author = obj.author
    return [
        author.get_full_name(),
        author.email,
        author.initials,  # short text / initials
        {"path": author.avatar.url} if author.avatar else None,  # avatar image
    ]
```
