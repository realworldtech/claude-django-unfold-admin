---
name: unfold-admin
description: This skill should be used when the user asks to "create a Django admin", "build an admin page", "style admin with unfold", "add admin actions", "customize admin filters", or mentions django-unfold, unfold admin, or admin theming.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Django Unfold Admin Skill

This skill helps you build modern, beautifully styled Django admin interfaces using django-unfold. Unfold provides a complete redesign of Django's admin with Tailwind CSS styling, Material Symbols icons, and enhanced functionality.

## CRITICAL: Before Writing Any Code

**STOP and read the correct reference file FIRST:**

- **Writing/fixing HTML templates?** → Read `references/templates-and-components.md`
- **Styling forms or widgets?** → Read `references/widgets-and-styling.md`
- **Adding admin actions?** → Read `references/actions-and-decorators.md`
- **Adding filters?** → Read `references/filters-and-search.md`
- **Configuring settings?** → Read `references/settings-configuration.md`

**DO NOT guess at Tailwind classes or HTML patterns.** The reference files contain the exact classes and patterns that match Unfold's styling. Using Bootstrap or generic Tailwind will look wrong.

## Quick Start

### Installation

```bash
pip install django-unfold
```

### Settings Configuration

Add `unfold` before `django.contrib.admin` in INSTALLED_APPS:

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",  # Optional: advanced filters
    "unfold.contrib.import_export",  # Optional: styled import/export forms
    "django.contrib.admin",
    # ... other apps
]
```

### User & Group Admin (Always Do This)

**Every Unfold project must re-register the User and Group admin.** Without this, the auth pages use Django's unstyled admin and look broken. Do this as part of initial setup, before writing any other ModelAdmin classes.

In your main `admin.py` (or a dedicated `accounts/admin.py`):

```python
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
```

If the project uses a custom user model (`AUTH_USER_MODEL`), see `examples/user-admin.py` for `AbstractUser` and `AbstractBaseUser` patterns.

### Basic ModelAdmin

Always inherit from `unfold.admin.ModelAdmin` instead of Django's default:

```python
from django.contrib import admin
from unfold.admin import ModelAdmin

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin):
    list_display = ["name", "status", "created_at"]
    search_fields = ["name"]
```

## Third-Party Admin Compatibility (Auto-Detect)

**When bootstrapping Unfold or enabling it on an existing project, ALWAYS scan for third-party apps that register their own admin classes.** These will render with Django's unstyled admin and look broken alongside Unfold-styled pages.

### Detection

Check the project's `INSTALLED_APPS` for these packages and apply the correct fix:

| Package | App in INSTALLED_APPS | Fix type |
|---------|----------------------|----------|
| django-celery-beat | `django_celery_beat` | Unregister & re-register 5 models + widget overrides |
| django-celery-results | `django_celery_results` | Unregister & re-register 2 models |
| django-simple-history | `simple_history` | Add `unfold.contrib.simple_history` to INSTALLED_APPS + multiple inheritance |
| django-modeltranslation | `modeltranslation` | Multiple inheritance with `TabbedTranslationAdmin` |
| django-import-export | `import_export` | Multiple inheritance + unfold form classes (see Section 9) |
| django-guardian | `guardian` | Add `unfold.contrib.guardian` to INSTALLED_APPS |
| django-constance | `constance` | Add `unfold.contrib.constance` before `constance` + use `UNFOLD_CONSTANCE_ADDITIONAL_FIELDS` |
| django-location-field | `location_field` | Add `unfold.contrib.location_field` + use `UnfoldAdminLocationWidget` |
| django-money | `djmoney` | **Automatic** — no changes needed |
| djangoql | `djangoql` | **Automatic** — no changes needed |
| django-json-widget | `django_json_widget` | **Automatic** — no changes needed |

Also grep the project for any `admin.site.register()` calls or `@admin.register` decorators where the admin class inherits from `django.contrib.admin.ModelAdmin` instead of `unfold.admin.ModelAdmin`.

### Fix Pattern

The general fix for apps that register their own admin:

1. **Unregister** the default admin class
2. **Re-register** with a class that inherits from BOTH the original third-party admin AND `unfold.admin.ModelAdmin`
3. **MRO order matters**: third-party base admin first, then `ModelAdmin`

```python
from django.contrib import admin
from unfold.admin import ModelAdmin
from some_package.admin import SomeModelAdmin as BaseSomeModelAdmin
from some_package.models import SomeModel

admin.site.unregister(SomeModel)

@admin.register(SomeModel)
class SomeModelAdmin(BaseSomeModelAdmin, ModelAdmin):
    pass
```

### django-celery-beat + django-celery-results

This is the most common case. See `examples/third-party-admin.py` for the complete solution.

**Important**: The PeriodicTask admin needs custom widget and form overrides — without these, the task selector fields render unstyled. This follows the [official Unfold guide](https://unfoldadmin.com/docs/integrations/django-celery-beat/).

```python
# In your admin.py (or a dedicated celery_admin.py)
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget

# --- celery beat ---
from django_celery_beat.admin import (
    ClockedScheduleAdmin as BaseClockedScheduleAdmin,
    CrontabScheduleAdmin as BaseCrontabScheduleAdmin,
    PeriodicTaskAdmin as BasePeriodicTaskAdmin,
    PeriodicTaskForm,
    TaskSelectWidget,
)
from django_celery_beat.models import (
    ClockedSchedule, CrontabSchedule, IntervalSchedule,
    PeriodicTask, SolarSchedule,
)

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm

@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass

@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass

@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass

@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass

# --- celery results (same pattern, no widget overrides needed) ---
from django_celery_results.admin import (
    GroupResultAdmin as BaseGroupResultAdmin,
    TaskResultAdmin as BaseTaskResultAdmin,
)
from django_celery_results.models import GroupResult, TaskResult

admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)

@admin.register(TaskResult)
class TaskResultAdmin(BaseTaskResultAdmin, ModelAdmin):
    pass

@admin.register(GroupResult)
class GroupResultAdmin(BaseGroupResultAdmin, ModelAdmin):
    pass
```

### django-simple-history

Requires `unfold.contrib.simple_history` in INSTALLED_APPS (after `unfold`, before `simple_history`):

```python
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin

@admin.register(MyModel)
class MyModelAdmin(SimpleHistoryAdmin, ModelAdmin):
    pass
```

### django-modeltranslation

```python
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin, TabbedTranslationAdmin):
    pass
```

### When to Apply This

- **During initial Unfold setup**: scan INSTALLED_APPS and fix all third-party admin classes before the user sees broken pages
- **When adding a new third-party app**: check if it registers admin classes and apply the pattern
- **When debugging "some admin pages look unstyled"**: this is almost always the cause

## Core Concepts

### 1. Class Inheritance

**Critical**: Always use unfold classes, not Django's built-ins:

| Django Class | Unfold Replacement |
|--------------|-------------------|
| `admin.ModelAdmin` | `unfold.admin.ModelAdmin` |
| `admin.TabularInline` | `unfold.admin.TabularInline` |
| `admin.StackedInline` | `unfold.admin.StackedInline` |

For generic inlines, use `unfold.admin.GenericStackedInline` and `unfold.admin.GenericTabularInline`.

**Note:** For import/export, there is no unfold replacement class. Use multiple inheritance: `class MyAdmin(ModelAdmin, ImportExportModelAdmin)` — see Section 9.

### 2. Actions System

Unfold provides four action placement locations:

| Location | Attribute | Signature |
|----------|-----------|-----------|
| Top of changelist | `actions_list` | `def action(self, request)` |
| Per-row in table | `actions_row` | `def action(self, request, object_id)` |
| Top of change form | `actions_detail` | `def action(self, request, object_id)` |
| Form submit line | `actions_submit_line` | `def action(self, request, obj)` |

**Action Decorator Options**:

```python
from unfold.decorators import action
from unfold.enums import ActionVariant

@action(
    description="Export Selected",
    permissions=["export"],
    url_path="export",
    icon="download",
    variant=ActionVariant.PRIMARY  # DEFAULT, PRIMARY, SUCCESS, INFO, WARNING, DANGER
)
def export_action(self, request, object_id):
    # Implementation
    return redirect(...)
```

**Dropdown Actions** - Group related actions:

```python
actions_detail = [
    "single_action",
    {
        "title": "More Actions",
        "items": ["action_one", "action_two"],
    },
]
```

### 3. Display Decorator

Customize how fields appear in list views:

```python
from unfold.decorators import display

@display(description="Status", label=True)
def display_status(self, obj):
    return obj.status  # Renders as colored badge

@display(header=True)
def display_header(self, obj):
    return obj.title, obj.subtitle  # Two-line header display

@display(boolean=True)
def display_active(self, obj):
    return obj.is_active  # Icon indicator

@display(label={"draft": "warning", "published": "success"})
def display_state(self, obj):
    return obj.state  # Custom label colors per value
```

### 4. Filters (unfold.contrib.filters)

Import all filters from `unfold.contrib.filters.admin`:

**Dropdown Filters**:
- `DropdownFilter` - Custom dropdown (subclass and implement `lookups()` and `queryset()`)
- `ChoicesDropdownFilter` - For choice fields
- `RelatedDropdownFilter` - For foreign keys
- `MultipleDropdownFilter` - Multiple selection
- `MultipleChoicesDropdownFilter` - Multiple choice selection
- `MultipleRelatedDropdownFilter` - Multiple foreign key selection

**Radio/Checkbox Filters**:
- `RadioFilter` - Single selection radio buttons
- `CheckboxFilter` - Multiple selection checkboxes
- `ChoicesRadioFilter` - Radio for choice fields
- `ChoicesCheckboxFilter` - Checkbox for choice fields
- `BooleanRadioFilter` - Yes/No/All for boolean fields
- `RelatedCheckboxFilter` - Checkbox for related fields
- `AllValuesCheckboxFilter` - Checkbox for all unique values

**Date/Time Filters**:
- `RangeDateFilter` - Date range picker (requires `DateField`)
- `RangeDateTimeFilter` - DateTime range picker (requires `DateTimeField`)

**Numeric Filters**:
- `SingleNumericFilter` - Single number input
- `RangeNumericFilter` - Number range (from/to)
- `RangeNumericListFilter` - Standalone numeric range
- `SliderNumericFilter` - Interactive slider

**Text Filters**:
- `TextFilter` - Custom text search (subclass and implement)
- `FieldTextFilter` - Text search on specific field

**Autocomplete Filters**:
- `AutocompleteSelectFilter` - Autocomplete single select
- `AutocompleteSelectMultipleFilter` - Autocomplete multi-select

Example:

```python
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    RangeDateFilter,
    SliderNumericFilter,
)

class MyModelAdmin(ModelAdmin):
    list_filter = [
        ("status", ChoicesDropdownFilter),
        ("created_at", RangeDateFilter),
        ("price", SliderNumericFilter),
    ]
    list_filter_submit = True  # Add apply button
    list_filter_sheet = True   # Show filters in sheet (default)
```

### 5. Fieldsets and Tabs

Organize form fields using fieldsets with special classes:

```python
fieldsets = (
    (None, {"fields": ("name", "slug")}),
    ("Details", {
        "fields": ("description", "category"),
        "classes": ["tab"],  # Renders as tab
    }),
    ("Advanced", {
        "fields": ("metadata",),
        "classes": ["collapse"],  # Collapsible section
    }),
)
```

### 6. Inlines

```python
from unfold.admin import TabularInline, StackedInline

class ItemInline(TabularInline):
    model = Item
    extra = 0
    per_page = 10  # Pagination
    collapsible = True  # Can collapse
    ordering_field = "position"  # Drag-drop ordering
    hide_ordering_field = True
    tab = True  # Show as tab
```

### 7. Sections (Change Form)

Add extra content sections to change forms:

```python
from unfold.sections import TableSection, TemplateSection

class RelatedItemsSection(TableSection):
    verbose_name = "Related Items"
    related_name = "items"  # Related manager name
    fields = ["name", "price"]
    height = "300px"

class CustomSection(TemplateSection):
    template_name = "admin/custom_section.html"

class MyModelAdmin(ModelAdmin):
    list_sections = [RelatedItemsSection, CustomSection]
```

### 8. Datasets (Change Form)

Embed another model's changelist in a change form:

```python
from unfold.datasets import BaseDataset

class RelatedItemDataset(BaseDataset):
    model = Item
    model_admin = ItemModelAdmin  # Must be unfold ModelAdmin
    tab = True  # Show as tab

class MyModelAdmin(ModelAdmin):
    change_form_datasets = [RelatedItemDataset]
```

### 9. Import/Export Integration (django-import-export)

Unfold does **not** provide its own `ImportExportModelAdmin`. Instead, use multiple inheritance with the standard `import_export.admin.ImportExportModelAdmin` and unfold's `ModelAdmin`. The `unfold.contrib.import_export` app provides template overrides and styled form classes — no custom admin class needed.

**Setup:**

1. Install: `pip install django-import-export`
2. Add `"unfold.contrib.import_export"` to `INSTALLED_APPS` (before `django.contrib.admin`)
3. Use multiple inheritance and set the form classes:

```python
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    # ... rest of your admin config
```

**Key points:**
- Inherit `ModelAdmin` first, then `ImportExportModelAdmin` (MRO order matters)
- `ImportForm` and `ExportForm` from `unfold.contrib.import_export.forms` style the import/export pages to match Unfold
- For field-selectable exports, use `SelectableFieldsExportForm` instead of `ExportForm`
- `ExportActionModelAdmin` was removed in django-import-export 4.x+ — use the default export action directly

## Styling Guidelines

### Icons

Use Material Symbols names (not Material Icons):
- Common: `dashboard`, `person`, `settings`, `edit`, `delete`, `add`, `check`, `close`
- Full list: https://fonts.google.com/icons

### Colors (OKLch System)

Unfold uses OKLch colors. Configure in settings:

```python
UNFOLD = {
    "COLORS": {
        "primary": {
            "50": "oklch(97.7% .014 308.299)",
            # ... 100-950 shades
        },
    },
}
```

### Tailwind CSS

Use Tailwind utility classes in templates and custom widgets. Support dark mode with `dark:` prefix.

## ModelAdmin Attributes Reference

| Attribute | Type | Description |
|-----------|------|-------------|
| `actions_list` | list | Actions at top of changelist |
| `actions_row` | list | Actions per row |
| `actions_detail` | list | Actions on change form |
| `actions_submit_line` | list | Actions in submit line |
| `list_filter_submit` | bool | Show apply button for filters |
| `list_filter_sheet` | bool | Show filters in side sheet |
| `list_fullwidth` | bool | Full-width list table |
| `list_horizontal_scrollbar_top` | bool | Scrollbar at top |
| `list_disable_select_all` | bool | Disable select all checkbox |
| `list_before_template` | str | Template before list |
| `list_after_template` | str | Template after list |
| `change_form_before_template` | str | Template before form |
| `change_form_after_template` | str | Template after form |
| `ordering_field` | str | Field for drag-drop ordering |
| `hide_ordering_field` | bool | Hide ordering column |
| `compressed_fields` | bool | Compact field display |
| `warn_unsaved_form` | bool | Warn on unsaved changes |
| `add_fieldsets` | tuple | Fieldsets for add form |
| `readonly_preprocess_fields` | dict | Preprocess readonly fields |

## Query Optimization (select_related / prefetch_related)

When building admin interfaces, consider whether query optimization is needed. **Do not blindly add `select_related` or `prefetch_related`** - assess the actual query patterns first.

### When to Investigate

Before adding optimization, check:
1. **How many queries are being made?** Use Django Debug Toolbar or `django.db.connection.queries`
2. **Is there an N+1 problem?** Look for repeated queries in loops
3. **What fields are actually displayed?** Only optimize for fields shown in `list_display`

### Assessment Checklist

```python
# Ask yourself:
# 1. Does list_display reference ForeignKey fields? → Consider select_related
# 2. Does list_display reference reverse relations or M2M? → Consider prefetch_related
# 3. Are custom display methods accessing related objects? → Check each one
# 4. Is the changelist slow with many records? → Profile first, then optimize
```

### Implementation

Override `get_queryset()` only when optimization is confirmed necessary:

```python
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["id", "customer_name", "product_count", "created_at"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # select_related for ForeignKey (single object)
        # prefetch_related for reverse FK or M2M (multiple objects)
        return qs.select_related("customer").prefetch_related("items")

    @display(description="Customer")
    def customer_name(self, obj):
        return obj.customer.name  # Uses select_related

    @display(description="Items")
    def product_count(self, obj):
        return obj.items.count()  # Uses prefetch_related
```

### Key Differences

| Method | Use For | Joins |
|--------|---------|-------|
| `select_related` | ForeignKey, OneToOne | SQL JOIN (single query) |
| `prefetch_related` | ManyToMany, reverse FK | Separate query + Python join |

### Red Flags (Signs You Need Optimization)

- Changelist page loads slowly
- Debug toolbar shows dozens/hundreds of queries
- Same table queried repeatedly with different IDs

### When NOT to Optimize

- Small datasets (< 100 records typically visible)
- Fields not shown in list_display
- Admin is rarely used
- Premature optimization without profiling

**Principle**: Measure first, optimize second. Adding unnecessary `select_related` can actually hurt performance if selecting large related objects that aren't used.

## User & Group Admin

Django's built-in User and Group admin must be re-registered with Unfold to get proper styling. This is required in every Unfold project.

### Minimum Setup (Default User)

```python
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
```

### Key Rules

1. **Always inherit from both** the Django base admin class AND `unfold.admin.ModelAdmin` (order matters — Django base first)
2. **Always set the three forms**: `form`, `add_form`, `change_password_form` from `unfold.forms`
3. **Always unregister first** before re-registering
4. **Custom User models** extending `AbstractUser`: keep `BaseUserAdmin` inheritance, add custom fields to `fieldsets` and `add_fieldsets`
5. **Custom User models** extending `AbstractBaseUser`: keep `BaseUserAdmin` inheritance but fully define `fieldsets`, `add_fieldsets`, `list_display`, `search_fields`, and `ordering` since the defaults assume a `username` field

See `examples/user-admin.py` for complete examples of all three scenarios (default User, AbstractUser, AbstractBaseUser).

## IMPORTANT: Which Reference to Use

**You MUST read the appropriate reference file before writing code.** Match the task to the correct file:

| Task | READ THIS FILE FIRST |
|------|---------------------|
| Setting up User/Group admin | **`examples/user-admin.py`** |
| Fixing unstyled third-party admin pages (celery, etc.) | **`examples/third-party-admin.py`** |
| Writing HTML templates, styling buttons/cards/alerts, custom dashboard | **`references/templates-and-components.md`** |
| Customizing form widgets, input styling, CSS classes | **`references/widgets-and-styling.md`** |
| Adding @action or @display decorators to ModelAdmin | **`references/actions-and-decorators.md`** |
| Adding list_filter, search, filter classes | **`references/filters-and-search.md`** |
| Configuring UNFOLD settings dict, sidebar, colors | **`references/settings-configuration.md`** |
| Inlines, TableSection, TemplateSection, BaseDataset | **`references/inlines-and-sections.md`** |
| Import/export with django-import-export | **Section 9 above** (multiple inheritance + unfold form classes) |

**For HTML/template work:** ALWAYS read `references/templates-and-components.md` first. It contains:
- Tailwind CSS class patterns for Unfold
- Component examples (cards, badges, buttons, tables, alerts)
- Dark mode patterns (`dark:` prefix)
- Material Symbols icon names

**For Python ModelAdmin code:** Read `references/actions-and-decorators.md` for decorators, or look at `examples/advanced-admin.py` for full patterns.

## Example Files

| File | Use For |
|------|---------|
| `examples/user-admin.py` | **User & Group admin setup (default, AbstractUser, AbstractBaseUser)** |
| `examples/basic-admin.py` | Simple ModelAdmin Python patterns |
| `examples/third-party-admin.py` | **Fixing django-celery-beat, django-celery-results, and other third-party admin classes** |
| `examples/advanced-admin.py` | Full-featured admin with actions, filters, inlines |
| `examples/settings-example.py` | Complete UNFOLD settings configuration |
| `examples/custom-dashboard.html` | **HTML template patterns and Tailwind styling** |
