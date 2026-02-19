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

| Option | Type | Description |
|--------|------|-------------|
| `extra` | int | Number of empty forms |
| `per_page` | int | Pagination (items per page) |
| `collapsible` | bool | Can collapse inline section |
| `tab` | bool | Show as tab |
| `ordering_field` | str | Field for drag-drop ordering |
| `hide_ordering_field` | bool | Hide ordering column |
| `readonly_preprocess_fields` | dict | Preprocess readonly fields |

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

### Complete Inline Example

```python
class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    per_page = 5
    collapsible = True
    ordering_field = "position"
    hide_ordering_field = True

    fields = ["product", "quantity", "price", "position"]
    readonly_fields = ["price"]
    autocomplete_fields = ["product"]

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("position")
```

---

## Sections

Sections add extra content to change list pages (below the list).

### Import

```python
from unfold.sections import TableSection, TemplateSection
```

### TableSection

Display related data as a table:

```python
class RelatedOrdersSection(TableSection):
    verbose_name = "Recent Orders"
    related_name = "orders"  # Related manager name on model
    fields = ["id", "total", "created_at"]
    height = "300px"  # Optional fixed height

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
| `model_admin` | ModelAdmin class | Admin class for display config |
| `tab` | bool | Show as tab (default: False) |

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
    height = "200px"

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
