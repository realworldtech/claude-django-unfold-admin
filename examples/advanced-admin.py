"""
Advanced Django Unfold Admin Example

This example demonstrates a full-featured ModelAdmin with actions,
filters, inlines, sections, and datasets.
"""

from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.filters.admin import (
    AutocompleteSelectFilter,
    ChoicesDropdownFilter,
    RangeDateFilter,
    SliderNumericFilter,
)
from unfold.datasets import BaseDataset
from unfold.decorators import action, display
from unfold.enums import ActionVariant
from unfold.sections import TableSection, TemplateSection

from .models import Order, OrderItem, Payment, Product


# =============================================================================
# Inlines
# =============================================================================


class OrderItemInline(TabularInline):
    """Inline for order items with pagination and ordering."""

    model = OrderItem
    extra = 0
    per_page = 5
    collapsible = True
    ordering_field = "position"
    hide_ordering_field = True

    fields = ["product", "quantity", "unit_price", "total_price", "position"]
    readonly_fields = ["total_price"]
    autocomplete_fields = ["product"]

    @display(description="Total")
    def total_price(self, obj):
        return f"${obj.quantity * obj.unit_price:.2f}"


# =============================================================================
# Sections
# =============================================================================


class OrderHistorySection(TableSection):
    """Display order history as a table section."""

    verbose_name = "Order History"
    related_name = "orders"
    fields = ["order_number", "total_display", "status_display", "created_at"]
    height = "250px"

    @display(description="Order #")
    def order_number(self, obj):
        return f"#{obj.id:05d}"

    @display(description="Total")
    def total_display(self, obj):
        return f"${obj.total:.2f}"

    @display(description="Status")
    def status_display(self, obj):
        return obj.get_status_display()


class CustomerStatsSection(TemplateSection):
    """Custom template section for customer statistics."""

    template_name = "admin/shop/customer_stats.html"


# =============================================================================
# Datasets
# =============================================================================


class PaymentDatasetModelAdmin(ModelAdmin):
    """ModelAdmin used within the Payment dataset."""

    list_display = ["payment_id", "amount_display", "method", "status", "created_at"]
    list_per_page = 5

    @display(description="ID")
    def payment_id(self, obj):
        return f"PAY-{obj.id:06d}"

    @display(description="Amount")
    def amount_display(self, obj):
        return f"${obj.amount:.2f}"


class PaymentsDataset(BaseDataset):
    """Embed payments changelist in order change form."""

    model = Payment
    model_admin = PaymentDatasetModelAdmin
    tab = True


# =============================================================================
# Main Admin Classes
# =============================================================================


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """Product admin with search for autocomplete support."""

    list_display = ["name", "sku", "price_display", "stock", "is_active"]
    search_fields = ["name", "sku"]  # Required for autocomplete
    list_filter = ["is_active", "category"]

    @display(description="Price")
    def price_display(self, obj):
        return f"${obj.price:.2f}"


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """
    Full-featured order admin with all unfold capabilities.
    """

    # List view
    list_display = [
        "order_number",
        "display_customer",
        "display_total",
        "display_status",
        "display_paid",
        "created_at",
    ]
    list_display_links = ["order_number"]
    list_filter = [
        ("status", ChoicesDropdownFilter),
        ("customer", AutocompleteSelectFilter),
        ("created_at", RangeDateFilter),
        ("total", SliderNumericFilter),
    ]
    search_fields = ["id", "customer__email", "customer__name"]
    date_hierarchy = "created_at"

    # Filter options
    list_filter_submit = True
    list_filter_sheet = True
    list_fullwidth = True

    # Inlines and datasets
    inlines = [OrderItemInline]
    change_form_datasets = [PaymentsDataset]

    # Form configuration with tabs
    fieldsets = (
        (None, {
            "fields": ("customer", "status"),
        }),
        (_("Order Details"), {
            "fields": (("subtotal", "tax"), "shipping", "total"),
            "classes": ["tab"],
        }),
        (_("Shipping Address"), {
            "fields": ("shipping_name", "shipping_address", "shipping_city",
                      "shipping_country", "shipping_postal_code"),
            "classes": ["tab"],
        }),
        (_("Notes"), {
            "fields": ("customer_notes", "internal_notes"),
            "classes": ["tab", "collapse"],
        }),
    )
    readonly_fields = ["subtotal", "tax", "total"]
    autocomplete_fields = ["customer"]

    # Template hooks
    change_form_before_template = "admin/shop/order_summary.html"

    # Actions placement
    actions_list = ["export_orders", "generate_report"]
    actions_row = ["view_invoice", "send_confirmation"]
    actions_detail = [
        "mark_shipped",
        "send_tracking",
        {
            "title": "More Actions",
            "items": ["refund_order", "cancel_order"],
        },
    ]
    actions_submit_line = ["save_and_send_confirmation"]

    # =========================================================================
    # Display Methods
    # =========================================================================

    @display(description="Order")
    def order_number(self, obj):
        return f"#{obj.id:05d}"

    @display(description="Customer", header=True)
    def display_customer(self, obj):
        return obj.customer.name, obj.customer.email

    @display(description="Total")
    def display_total(self, obj):
        return f"${obj.total:.2f}"

    @display(
        description="Status",
        label={
            "pending": "warning",
            "processing": "info",
            "shipped": "primary",
            "delivered": "success",
            "cancelled": "danger",
        }
    )
    def display_status(self, obj):
        return obj.status

    @display(description="Paid", boolean=True)
    def display_paid(self, obj):
        return obj.is_paid

    # =========================================================================
    # Changelist Actions
    # =========================================================================

    @action(
        description="Export Orders",
        icon="download",
        variant=ActionVariant.PRIMARY,
    )
    def export_orders(self, request):
        messages.success(request, "Orders exported successfully.")
        return redirect(reverse_lazy("admin:shop_order_changelist"))

    @action(description="Generate Report", icon="assessment")
    def generate_report(self, request):
        messages.info(request, "Report generation started.")
        return redirect(reverse_lazy("admin:shop_order_changelist"))

    # =========================================================================
    # Row Actions
    # =========================================================================

    @action(description="Invoice", icon="receipt")
    def view_invoice(self, request, object_id):
        return redirect(f"/invoices/{object_id}/")

    @action(description="Confirm", icon="email")
    def send_confirmation(self, request, object_id):
        messages.success(request, f"Confirmation sent for order #{object_id}.")
        return redirect(reverse_lazy("admin:shop_order_changelist"))

    # =========================================================================
    # Detail Actions
    # =========================================================================

    @action(
        description="Mark as Shipped",
        icon="local_shipping",
        variant=ActionVariant.SUCCESS,
        permissions=["change"],
    )
    def mark_shipped(self, request, object_id):
        order = self.get_object(request, object_id)
        order.status = "shipped"
        order.save()
        messages.success(request, f"Order #{object_id} marked as shipped.")
        return redirect(reverse_lazy("admin:shop_order_change", args=[object_id]))

    @action(description="Send Tracking", icon="track_changes")
    def send_tracking(self, request, object_id):
        messages.success(request, "Tracking information sent.")
        return redirect(reverse_lazy("admin:shop_order_change", args=[object_id]))

    @action(
        description="Refund Order",
        icon="currency_exchange",
        variant=ActionVariant.WARNING,
        permissions=["refund"],
    )
    def refund_order(self, request, object_id):
        messages.warning(request, f"Refund initiated for order #{object_id}.")
        return redirect(reverse_lazy("admin:shop_order_change", args=[object_id]))

    @action(
        description="Cancel Order",
        icon="cancel",
        variant=ActionVariant.DANGER,
        permissions=["delete"],
    )
    def cancel_order(self, request, object_id):
        order = self.get_object(request, object_id)
        order.status = "cancelled"
        order.save()
        messages.error(request, f"Order #{object_id} cancelled.")
        return redirect(reverse_lazy("admin:shop_order_change", args=[object_id]))

    def has_refund_permission(self, request, object_id=None):
        return request.user.has_perm("shop.refund_order")

    # =========================================================================
    # Submit Line Actions
    # =========================================================================

    @action(description="Save & Send Confirmation")
    def save_and_send_confirmation(self, request, obj):
        # obj is the saved instance
        messages.success(request, f"Order saved and confirmation sent to {obj.customer.email}.")
