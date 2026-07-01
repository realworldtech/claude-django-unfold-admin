"""
Basic Django Unfold Admin Example

This example demonstrates a simple ModelAdmin setup with common patterns.
"""

from django.contrib import admin

from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    """Simple ModelAdmin for Category model."""

    list_display = ["name", "slug", "article_count"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

    @display(description="Articles")
    def article_count(self, obj):
        return obj.articles.count()


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    """
    Basic ModelAdmin with common unfold patterns.
    """

    # List view configuration
    list_display = [
        "title",
        "category",
        "display_status",
        "display_published",
        "created_at",
    ]
    list_display_links = ["title"]
    list_filter = ["status", "category", "created_at"]
    search_fields = ["title", "content"]
    date_hierarchy = "created_at"

    # Form configuration
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "category"),
        }),
        ("Content", {
            "fields": ("content", "excerpt"),
        }),
        ("Publishing", {
            "fields": ("status", "published_at"),
        }),
    )
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["category"]
    readonly_fields = ["created_at", "updated_at"]

    # Display decorators for custom column rendering
    @display(description="Status", label=True)
    def display_status(self, obj):
        """Display status as a colored label."""
        return obj.get_status_display()

    @display(description="Published", boolean=True)
    def display_published(self, obj):
        """Display published state as boolean icon."""
        return obj.status == "published"
