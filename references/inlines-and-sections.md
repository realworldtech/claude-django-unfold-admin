# Inlines, Sections, and Datasets Reference

## Inlines

### Basic Usage

Always use unfold inline classes:

```python
from unfold.admin import ModelAdmin, TabularInline, StackedInline

class ItemInline(TabularInline):  # or StackedInline
    model = Item
    extra = 0

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = [ItemInline]
```

### Available Classes

```python
from unfold.admin import (
    TabularInline,          # Table-style inline
    StackedInline,          # Stacked form inline
    GenericTabularInline,   # For GenericForeignKey
    GenericStackedInline,   # For GenericForeignKey
)
```

### Inline Options

These are the Unfold-specific attributes (all live on `BaseInlineMixin`), in addition to the standard Django inline options:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `extra` | int | (Django) | Number of empty forms |
| `per_page` | int | `None` | Enable pagination (items per page) |
| `collapsible` | bool | `False` | Can collapse the inline section |
| `tab` | bool | `False` | Render the inline inside a tab |
| `show_count` | bool | `False` | Show an object-count badge on the inline header |
| `hide_title` | bool | `False` | Hide the inline title row |
| `ordering_field` | str | `None` | Field for drag-drop ordering (saved records only) |
| `hide_ordering_field` | bool | `False` | Hide the ordering column |
| `readonly_preprocess_fields` | dict | `{}` | Preprocess readonly field values |

Customise the count badge with `get_count(request, obj)` and `get_count_variant(request, obj)` (returning `"primary"`/`"danger"`/`"success"`/`"info"`/`"warning"`); set a custom inline title with `get_inline_title()` on the **model**.

### Pagination

```python
class ItemInline(TabularInline):
    model = Item
    per_page = 10  # Show 10 items per page
```

### Collapsible

```python
class ItemInline(TabularInline):
    model = Item
    collapsible = True  # Can collapse/expand
```

### Tab Display

```python
class ItemInline(TabularInline):
    model = Item
    tab = True  # Show as tab instead of inline section
```

### Drag-Drop Ordering

```python
class ItemInline(TabularInline):
    model = Item
    ordering_field = "position"  # Model must have this field
    hide_ordering_field = True   # Hide the position column

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("position")
```

### Nested Inlines

Declare an `inlines` attribute on an inline class to nest one inline inside another. **One level of nesting only** (parent → child); deeper nesting and nesting through M2M are not supported.

```python
from unfold.admin import ModelAdmin, TabularInline

class SubTaskInline(TabularInline):
    model = SubTask

class TaskInline(TabularInline):
    model = Task
    inlines = [SubTaskInline]   # nested one level

@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    inlines = [TaskInline]
```

### Complete Inline Example

```python
class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    per_page = 5          # paginate the inline (PaginationInlineFormSet under the hood)
    collapsible = True
    show_count = True
    ordering_field = "position"
    hide_ordering_field = True

    fields = ["product", "quantity", "price", "position"]
    readonly_fields = ["price"]
    autocomplete_fields = ["product"]

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("position")
```

---

## Paginator: InfinitePaginator

For very large tables, `InfinitePaginator` avoids the expensive `COUNT(*)` that Django runs to compute total pages — it renders only Previous/Next.

```python
from unfold.admin import ModelAdmin
from unfold.paginator import InfinitePaginator

@admin.register(Event)
class EventAdmin(ModelAdmin):
    paginator = InfinitePaginator       # standard Django `paginator` attribute
    show_full_result_count = False      # skip the total-count query
```

---

## Sortable Changelist

Drag-drop row ordering on the changelist (not just inlines). Set `ordering_field` to a `PositiveIntegerField` on the model.

```python
@admin.register(Page)
class PageAdmin(ModelAdmin):
    ordering_field = "weight"       # model needs PositiveIntegerField(..., db_index=True)
    hide_ordering_field = True      # hide the weight column
    list_display = ["title", "weight"]
```

---

## Conditional Fields

Show or hide form fields live (no reload) based on the value of another field. `conditional_fields` maps a field name to an Alpine.js boolean expression referencing other fields in the form.

```python
@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    fields = ["different_address", "country", "city", "address"]
    conditional_fields = {
        "country": "different_address == true",
        "city": "different_address == true",
        "address": "different_address == true",
    }
```

For multi-widget fields (e.g. a `SplitDateTimeField` named `date_start`), reference the sub-widgets by suffix: `date_start_0`, `date_start_1`.

---

## Sections (Expandable Changelist Rows)

`list_sections` adds **expandable rows to the changelist** — each record gets a toggle that reveals the section content for that row. This is *not* change-form content; to embed a related changelist inside a change form, use **Datasets** (below).

### Import

```python
from unfold.sections import TableSection, TemplateSection
```

Each section is constructed with `(request, instance)`, where `instance` is the row's model object.

### TableSection

Display related data as a table. `related_name` is **required** (the related manager on the row's model); `height` is an optional int (pixels).

```python
class RelatedOrdersSection(TableSection):
    verbose_name = "Recent Orders"
    related_name = "orders"  # related manager name on the model (required)
    fields = ["id", "total", "created_at"]
    height = 300             # optional fixed height (int, pixels)

@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_sections = [RelatedOrdersSection]
```

### TableSection with Custom Methods

```python
class OrderHistorySection(TableSection):
    verbose_name = "Order History"
    related_name = "orders"
    fields = ["order_number", "formatted_total", "status_display"]

    def order_number(self, obj):
        return f"#{obj.id:05d}"
    order_number.short_description = "Order #"

    def formatted_total(self, obj):
        return f"${obj.total:.2f}"
    formatted_total.short_description = "Total"

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = "Status"
```

### TemplateSection

Render custom template:

```python
class StatsSection(TemplateSection):
    template_name = "admin/customer_stats.html"

@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_sections = [StatsSection]
```

Template receives `request` and `instance`:

```html
<!-- templates/admin/customer_stats.html -->
<div class="p-4 bg-white dark:bg-base-900 rounded-default">
    <h3 class="text-lg font-semibold mb-4">Statistics</h3>
    <div class="grid grid-cols-3 gap-4">
        <div class="text-center">
            <div class="text-2xl font-bold">{{ instance.orders.count }}</div>
            <div class="text-sm text-base-500">Orders</div>
        </div>
        <!-- More stats -->
    </div>
</div>
```

### Multiple Sections

```python
class CustomerAdmin(ModelAdmin):
    list_sections = [
        RecentOrdersSection,
        ActivityLogSection,
        StatsSection,
    ]
```

---

## Datasets

Datasets embed another model's changelist within a change form.

### Import

```python
from unfold.datasets import BaseDataset
```

### Basic Dataset

```python
from unfold.admin import ModelAdmin
from unfold.datasets import BaseDataset

# First, create a ModelAdmin for the embedded model
class OrderItemModelAdmin(ModelAdmin):
    list_display = ["product", "quantity", "price"]
    list_per_page = 10

# Create the dataset
class OrderItemsDataset(BaseDataset):
    model = OrderItem
    model_admin = OrderItemModelAdmin
    tab = True  # Show as tab

# Use in parent admin
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    change_form_datasets = [OrderItemsDataset]
```

### Dataset Properties

| Property | Type | Description |
|----------|------|-------------|
| `model` | Model class | The model to display |
| `model_admin` | ModelAdmin class | Admin class for display config (must be an Unfold `ModelAdmin`) |
| `tab` | bool | Show as tab (default: `False`) |
| `title` | str | Custom title for the dataset |

> **Datasets disable list filters and column sorting.** The embedded changelist is built with `list_filter=[]` and `sortable_by=[]`. Don't rely on filtering/sorting inside a dataset; scope the rows via `get_queryset()` on the dataset's `model_admin` instead.

### Dataset with Actions

The embedded changelist supports actions:

```python
class OrderItemModelAdmin(ModelAdmin):
    list_display = ["product", "quantity", "price"]
    actions = ["mark_shipped"]

    @admin.action(description="Mark as shipped")
    def mark_shipped(self, request, queryset):
        queryset.update(shipped=True)
```

### Multiple Datasets

```python
class OrderItemsDataset(BaseDataset):
    model = OrderItem
    model_admin = OrderItemModelAdmin
    tab = True

class PaymentsDataset(BaseDataset):
    model = Payment
    model_admin = PaymentModelAdmin
    tab = True

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    change_form_datasets = [OrderItemsDataset, PaymentsDataset]
```

### Combining with Tabs

Datasets with `tab = True` appear as tabs alongside fieldset tabs:

```python
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    fieldsets = (
        (None, {"fields": ("customer", "status")}),
        ("Shipping", {
            "fields": ("address", "city", "country"),
            "classes": ["tab"],
        }),
        ("Notes", {
            "fields": ("internal_notes",),
            "classes": ["tab"],
        }),
    )

    change_form_datasets = [
        OrderItemsDataset,  # tab = True
        PaymentsDataset,    # tab = True
    ]
    # Results in tabs: General | Shipping | Notes | Order Items | Payments
```

---

## Complete Example

```python
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.datasets import BaseDataset
from unfold.sections import TableSection, TemplateSection

from .models import Customer, Order, OrderItem, Payment

# Inline
class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    per_page = 5

# Section
class RecentOrdersSection(TableSection):
    verbose_name = "Recent Orders"
    related_name = "orders"
    fields = ["id", "total", "status", "created_at"]
    height = 200

# Dataset ModelAdmin
class PaymentDatasetAdmin(ModelAdmin):
    list_display = ["amount", "method", "status", "created_at"]
    list_per_page = 5

# Dataset
class PaymentsDataset(BaseDataset):
    model = Payment
    model_admin = PaymentDatasetAdmin
    tab = True

# Main Admin
@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = ["name", "email", "total_orders"]
    list_sections = [RecentOrdersSection]

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["id", "customer", "total", "status"]
    inlines = [OrderItemInline]
    change_form_datasets = [PaymentsDataset]

    fieldsets = (
        (None, {"fields": ("customer", "status")}),
        ("Totals", {
            "fields": ("subtotal", "tax", "total"),
            "classes": ["tab"],
        }),
    )
```
