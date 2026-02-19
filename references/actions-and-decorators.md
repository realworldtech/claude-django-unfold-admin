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
| `attrs` | dict | Extra HTML attributes |

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
| `boolean` | bool | Display as boolean icon |
| `image` | bool | Display as image |
| `label` | bool/str/dict | Display as label/badge |
| `header` | bool | Display as two-line header |
| `dropdown` | bool | Display with dropdown content |
| `ordering` | str/expression | Enable sorting |
| `empty_value` | str | Value when empty |

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

Color mapping:
```python
@display(
    description="Status",
    label={
        "draft": "warning",     # Yellow
        "pending": "info",      # Blue
        "published": "success", # Green
        "archived": "danger",   # Red
    }
)
def display_status(self, obj):
    return obj.status
```

### Header Display

Two-line display with title and subtitle:

```python
@display(header=True)
def display_user(self, obj):
    return obj.full_name, obj.email  # Title, Subtitle
```

With image:
```python
@display(header=True)
def display_user(self, obj):
    return [
        obj.full_name,
        obj.email,
        obj.avatar.url if obj.avatar else None,  # Optional image
    ]
```

### Dropdown Display

Expandable content:

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
        author.avatar.url if author.avatar else None,
    ]
```
