# Widgets and Styling Reference

## Available Widgets

Import from `unfold.widgets`:

### Text Input Widgets

```python
from unfold.widgets import (
    UnfoldAdminTextInputWidget,         # Standard text input
    UnfoldAdminEmailInputWidget,        # Email input
    UnfoldAdminURLInputWidget,          # URL input with link preview
    UnfoldAdminUUIDInputWidget,         # UUID input
    UnfoldAdminPasswordWidget,          # Password input
    UnfoldAdminPasswordToggleWidget,    # Password input with show/hide toggle
    UnfoldAdminColorInputWidget,        # Color picker
)
```

### Numeric Widgets

```python
from unfold.widgets import (
    UnfoldAdminIntegerFieldWidget,    # Integer input
    UnfoldAdminDecimalFieldWidget,    # Decimal input
    UnfoldAdminBigIntegerFieldWidget, # Big integer input
    UnfoldAdminIntegerRangeWidget,    # Range (min/max) input
)
```

### Textarea Widgets

```python
from unfold.widgets import (
    UnfoldAdminTextareaWidget,           # Standard textarea
    UnfoldAdminExpandableTextareaWidget, # Auto-expanding textarea
)
```

### Date/Time Widgets

```python
from unfold.widgets import (
    UnfoldAdminDateWidget,                    # Date picker
    UnfoldAdminTimeWidget,                    # Time picker
    UnfoldAdminSingleDateWidget,              # Date without calendar
    UnfoldAdminSingleTimeWidget,              # Time without clock
    UnfoldAdminSplitDateTimeWidget,           # Horizontal date+time
    UnfoldAdminSplitDateTimeVerticalWidget,   # Vertical date+time
)
```

### Select Widgets

```python
from unfold.widgets import (
    UnfoldAdminSelectWidget,              # Standard select
    UnfoldAdminSelect2Widget,             # Select2 enhanced
    UnfoldAdminSelectMultipleWidget,      # Multiple select
    UnfoldAdminSelect2MultipleWidget,     # Select2 multiple
    UnfoldAdminNullBooleanSelectWidget,   # Yes/No/Unknown
    UnfoldAdminRadioSelectWidget,         # Radio buttons
)
```

### Checkbox Widgets

```python
from unfold.widgets import (
    UnfoldBooleanWidget,                     # Standard checkbox
    UnfoldBooleanSwitchWidget,               # Toggle switch
    UnfoldAdminCheckboxSelectMultipleWidget, # Checkbox group
)
```

### File Widgets

```python
from unfold.widgets import (
    UnfoldAdminFileFieldWidget,     # File upload
    UnfoldAdminImageFieldWidget,    # Image upload with preview
    UnfoldAdminImageSmallFieldWidget, # Small image upload
)
```

### Autocomplete Widgets

```python
from unfold.widgets import (
    UnfoldAdminAutocompleteWidget,                    # Single autocomplete
    UnfoldAdminMultipleAutocompleteWidget,            # Multiple autocomplete
    UnfoldAdminAutocompleteModelChoiceFieldWidget,    # ModelChoice autocomplete
    UnfoldAdminMultipleAutocompleteModelChoiceFieldWidget, # Multiple ModelChoice
)
```

### Relation Widgets

```python
from unfold.widgets import (
    UnfoldAdminRelatedFieldWrapperWidget,  # Related field wrapper (add/change/delete buttons)
    UnfoldForeignKeyRawIdWidget,           # Raw ID foreign key
)
```

### Money & Location Widgets

```python
from unfold.widgets import UnfoldAdminMoneyWidget   # requires django-money
from unfold.contrib.location_field.widgets import UnfoldAdminLocationWidget  # requires django-location-field
```

### Form Widgets (unfold.contrib.forms)

These live in `unfold.contrib.forms.widgets` and require `"unfold.contrib.forms"` in `INSTALLED_APPS`:

```python
from unfold.contrib.forms.widgets import (
    ArrayWidget,      # builds arrays of sub-widgets (e.g. Postgres ArrayField)
    WysiwygWidget,    # Trix rich-text editor
)
```

### JSON Fields

There is **no Unfold-specific JSON widget**. If you use **django-json-widget**, Unfold styles it automatically — just follow that package's own setup (nothing to add for Unfold).

## Using Widgets in Forms

```python
from django import forms
from unfold.widgets import (
    UnfoldAdminTextInputWidget,
    UnfoldAdminSelect2Widget,
    UnfoldBooleanSwitchWidget,
)

class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = "__all__"
        widgets = {
            "name": UnfoldAdminTextInputWidget(attrs={"placeholder": "Enter name"}),
            "category": UnfoldAdminSelect2Widget(choices=CATEGORY_CHOICES),
            "is_active": UnfoldBooleanSwitchWidget(),
        }
```

## Prefix/Suffix Support

Text input widgets support prefixes and suffixes:

```python
UnfoldAdminTextInputWidget(attrs={
    "prefix": "$",           # Text prefix
    "suffix": "USD",         # Text suffix
    "prefix_icon": "attach_money",  # Icon prefix (Material Symbol)
    "suffix_icon": "search",        # Icon suffix
})
```

## CSS Class Constants

Available for custom styling:

```python
from unfold.widgets import (
    BASE_CLASSES,         # Shared base classes
    BASE_INPUT_CLASSES,   # Shared input base (INPUT/TEXTAREA/SELECT build on this)
    INPUT_CLASSES,        # Text input styling
    TEXTAREA_CLASSES,     # Textarea styling
    SELECT_CLASSES,       # Select styling
    CHECKBOX_CLASSES,     # Checkbox styling
    RADIO_CLASSES,        # Radio button styling
    SWITCH_CLASSES,       # Toggle switch styling
    FILE_CLASSES,         # File input styling
    BUTTON_CLASSES,       # Button styling
    LABEL_CLASSES,        # Form label styling
    PROSE_CLASSES,        # Rich-text/prose styling
)
```

These are **lists of class strings** — join them when building a widget's `class` attribute (e.g. `" ".join([*INPUT_CLASSES, "my-extra"])`).

## Tailwind CSS Classes

Common patterns used in unfold widgets:

### Form Fields

```css
/* Input base */
border border-base-200 bg-white rounded-default shadow-xs
text-font-default-light text-sm font-medium
focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600
dark:bg-base-900 dark:border-base-700 dark:text-font-default-dark

/* Error state */
group-[.errors]:border-red-600
focus:group-[.errors]:outline-red-600
dark:group-[.errors]:border-red-500
```

### Buttons

```css
/* Primary button */
bg-primary-600 border-transparent text-white
font-medium px-3 py-2 rounded-default text-center
cursor-pointer whitespace-nowrap
```

### Checkbox

```css
appearance-none bg-white border border-base-300
rounded-[4px] h-4 w-4 cursor-pointer
checked:bg-primary-600 checked:border-primary-600
```

### Radio

```css
appearance-none bg-white border border-base-300
rounded-full h-4 w-4 cursor-pointer
checked:bg-primary-600 checked:border-primary-600
```

### Toggle Switch

```css
appearance-none bg-base-300 rounded-full
h-5 w-8 cursor-pointer transition-colors
checked:bg-green-500 dark:checked:bg-green-700
```

## Dark Mode

All styling supports dark mode via `dark:` prefix:

```html
<div class="bg-white dark:bg-base-900 text-base-900 dark:text-base-100">
```

## Material Symbols

Icons use Material Symbols (not Material Icons):

```html
<span class="material-symbols-outlined">dashboard</span>
```

Common icons:
- Navigation: `dashboard`, `home`, `menu`, `arrow_back`, `arrow_forward`
- Actions: `add`, `edit`, `delete`, `save`, `close`, `check`
- Content: `article`, `folder`, `image`, `description`
- Users: `person`, `people`, `group`, `admin_panel_settings`
- Status: `check_circle`, `error`, `warning`, `info`
- Files: `upload`, `download`, `attach_file`, `cloud_upload`

## Color System

Colors use CSS variables with OKLch values:

```css
/* Base palette */
var(--color-base-50) through var(--color-base-950)

/* Primary palette */
var(--color-primary-50) through var(--color-primary-950)

/* Font colors */
var(--color-font-subtle-light)
var(--color-font-subtle-dark)
var(--color-font-default-light)
var(--color-font-default-dark)
var(--color-font-important-light)
var(--color-font-important-dark)
```

## Custom Widget Example

```python
from django.forms import TextInput
from unfold.widgets import INPUT_CLASSES

class MyCustomWidget(TextInput):
    template_name = "widgets/my_custom.html"

    def __init__(self, attrs=None):
        default_attrs = {
            "class": " ".join([*INPUT_CLASSES, "my-custom-class"]),
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
```
