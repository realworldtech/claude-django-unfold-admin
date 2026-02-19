# Filters and Search Reference

## Installation

Add `unfold.contrib.filters` to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "django.contrib.admin",
    # ...
]
```

## Import

```python
from unfold.contrib.filters.admin import (
    # Dropdown filters
    DropdownFilter,
    ChoicesDropdownFilter,
    RelatedDropdownFilter,
    MultipleDropdownFilter,
    MultipleChoicesDropdownFilter,
    MultipleRelatedDropdownFilter,

    # Radio/Checkbox filters
    RadioFilter,
    CheckboxFilter,
    ChoicesRadioFilter,
    ChoicesCheckboxFilter,
    BooleanRadioFilter,
    RelatedCheckboxFilter,
    AllValuesCheckboxFilter,

    # Date/Time filters
    RangeDateFilter,
    RangeDateTimeFilter,

    # Numeric filters
    SingleNumericFilter,
    RangeNumericFilter,
    RangeNumericListFilter,
    SliderNumericFilter,

    # Text filters
    TextFilter,
    FieldTextFilter,

    # Autocomplete filters
    AutocompleteSelectFilter,
    AutocompleteSelectMultipleFilter,
)
```

## Filter Types

### Dropdown Filters

**ChoicesDropdownFilter** - For fields with `choices`:

```python
class MyModel(models.Model):
    STATUS_CHOICES = [("draft", "Draft"), ("published", "Published")]
    status = models.CharField(choices=STATUS_CHOICES)

class MyModelAdmin(ModelAdmin):
    list_filter = [("status", ChoicesDropdownFilter)]
```

**RelatedDropdownFilter** - For ForeignKey fields:

```python
list_filter = [("category", RelatedDropdownFilter)]
```

**MultipleChoicesDropdownFilter** - Multiple selection for choice fields:

```python
list_filter = [("tags", MultipleChoicesDropdownFilter)]
```

**MultipleRelatedDropdownFilter** - Multiple selection for FK/M2M:

```python
list_filter = [("categories", MultipleRelatedDropdownFilter)]
```

**Custom DropdownFilter**:

```python
class StatusDropdownFilter(DropdownFilter):
    title = "Status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("active", "Active"),
            ("inactive", "Inactive"),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

list_filter = [StatusDropdownFilter]
```

### Radio/Checkbox Filters

**ChoicesRadioFilter** - Radio buttons for choice fields:

```python
list_filter = [("priority", ChoicesRadioFilter)]
```

**ChoicesCheckboxFilter** - Checkboxes for choice fields:

```python
list_filter = [("tags", ChoicesCheckboxFilter)]
```

**BooleanRadioFilter** - Yes/No/All for boolean fields:

```python
list_filter = [("is_active", BooleanRadioFilter)]
```

**RelatedCheckboxFilter** - Checkboxes for related objects:

```python
list_filter = [("categories", RelatedCheckboxFilter)]
```

**AllValuesCheckboxFilter** - Checkboxes for all unique field values:

```python
list_filter = [("country", AllValuesCheckboxFilter)]
```

**Custom RadioFilter**:

```python
class PriorityRadioFilter(RadioFilter):
    title = "Priority Level"
    parameter_name = "priority"

    def lookups(self, request, model_admin):
        return [
            ("high", "High"),
            ("medium", "Medium"),
            ("low", "Low"),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(priority=self.value())
        return queryset
```

**Custom CheckboxFilter**:

```python
class TagCheckboxFilter(CheckboxFilter):
    title = "Tags"
    parameter_name = "tags"

    def lookups(self, request, model_admin):
        return Tag.objects.values_list("id", "name")

    def queryset(self, request, queryset):
        if self.value():  # Returns list for checkbox
            return queryset.filter(tags__in=self.value())
        return queryset
```

### Date/Time Filters

**RangeDateFilter** - For DateField:

```python
list_filter = [("created_at", RangeDateFilter)]
```

**RangeDateTimeFilter** - For DateTimeField:

```python
list_filter = [("updated_at", RangeDateTimeFilter)]
```

### Numeric Filters

**SingleNumericFilter** - Single number input:

```python
list_filter = [("quantity", SingleNumericFilter)]
```

**RangeNumericFilter** - Number range (from/to):

```python
list_filter = [("price", RangeNumericFilter)]
```

**SliderNumericFilter** - Interactive slider:

```python
list_filter = [("rating", SliderNumericFilter)]
```

Customizing slider:

```python
class CustomSliderFilter(SliderNumericFilter):
    MAX_DECIMALS = 2  # Decimal precision
    STEP = 0.5        # Step increment

list_filter = [("price", CustomSliderFilter)]
```

**RangeNumericListFilter** - Standalone range filter:

```python
class PriceRangeFilter(RangeNumericListFilter):
    title = "Price Range"
    parameter_name = "price_range"

    def queryset(self, request, queryset):
        # Access values via self.used_parameters
        from_val = self.used_parameters.get("price_range_from")
        to_val = self.used_parameters.get("price_range_to")

        if from_val:
            queryset = queryset.filter(price__gte=from_val)
        if to_val:
            queryset = queryset.filter(price__lte=to_val)
        return queryset
```

### Text Filters

**FieldTextFilter** - Text search on specific field:

```python
list_filter = [("title", FieldTextFilter)]  # Adds title__icontains filter
```

**Custom TextFilter**:

```python
class NameSearchFilter(TextFilter):
    title = "Search by Name"
    parameter_name = "name_search"

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__icontains=self.value())
        return queryset
```

### Autocomplete Filters

Requires `search_fields` on related model's admin:

```python
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    search_fields = ["name"]  # Required for autocomplete

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_filter = [
        ("category", AutocompleteSelectFilter),
        ("tags", AutocompleteSelectMultipleFilter),
    ]
```

## ModelAdmin Filter Options

```python
class MyModelAdmin(ModelAdmin):
    list_filter = [...]

    # Submit button for filters (good for many filters)
    list_filter_submit = True

    # Show filters in side sheet (default) vs inline
    list_filter_sheet = True  # True = sheet, False = inline
```

## Facet Counts

Django 5.0+ supports facet counts (showing count per filter option):

```python
class MyModelAdmin(ModelAdmin):
    list_filter = [("status", ChoicesDropdownFilter)]
    show_facets = admin.ShowFacets.ALWAYS  # or ALLOW, NEVER
```

## Complete Example

```python
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    MultipleRelatedDropdownFilter,
    RangeDateFilter,
    SliderNumericFilter,
    BooleanRadioFilter,
    FieldTextFilter,
    AutocompleteSelectFilter,
)

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ["name", "category", "price", "is_active", "created_at"]
    search_fields = ["name", "description"]

    list_filter = [
        ("name", FieldTextFilter),                    # Text search
        ("status", ChoicesDropdownFilter),            # Dropdown
        ("categories", MultipleRelatedDropdownFilter), # Multi-select related
        ("supplier", AutocompleteSelectFilter),       # Autocomplete
        ("price", SliderNumericFilter),               # Slider
        ("created_at", RangeDateFilter),              # Date range
        ("is_active", BooleanRadioFilter),            # Boolean radio
    ]

    list_filter_submit = True
    list_filter_sheet = True
```
