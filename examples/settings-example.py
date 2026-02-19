"""
Django Unfold Settings Example

Complete UNFOLD configuration for settings.py with all available options.
"""

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    # =========================================================================
    # Site Branding
    # =========================================================================
    "SITE_TITLE": "My Admin Panel",
    "SITE_HEADER": "My Company Admin",
    "SITE_SUBHEADER": "Management Dashboard",
    "SITE_URL": "/",

    # Site icon - choose ONE of the following options:

    # Option 1: Static image path
    # "SITE_ICON": lambda request: static("images/icon.svg"),

    # Option 2: Material Symbol name
    "SITE_SYMBOL": "dashboard",

    # Option 3: Logo with light/dark variants
    # "SITE_LOGO": {
    #     "light": {
    #         "url": lambda request: static("images/logo-light.svg"),
    #         "alt": "My Company",
    #         "height": 32,
    #     },
    #     "dark": {
    #         "url": lambda request: static("images/logo-dark.svg"),
    #         "alt": "My Company",
    #         "height": 32,
    #     },
    # },

    # Favicons
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: static("favicon/favicon-32x32.png"),
        },
        {
            "rel": "icon",
            "sizes": "16x16",
            "type": "image/png",
            "href": lambda request: static("favicon/favicon-16x16.png"),
        },
        {
            "rel": "apple-touch-icon",
            "sizes": "180x180",
            "href": lambda request: static("favicon/apple-touch-icon.png"),
        },
    ],

    # =========================================================================
    # Feature Toggles
    # =========================================================================
    "SHOW_HISTORY": True,         # Show history link in change forms
    "SHOW_VIEW_ON_SITE": True,    # Show "View on site" link
    "SHOW_BACK_BUTTON": False,    # Show back button in header

    # =========================================================================
    # Language Settings
    # =========================================================================
    "SHOW_LANGUAGES": True,
    "LANGUAGE_FLAGS": {
        "en": "us",  # Map language code to flag
        "es": "es",
        "fr": "fr",
        "de": "de",
    },

    # =========================================================================
    # Colors (OKLch Color System)
    # =========================================================================
    "COLORS": {
        # Base colors (gray scale)
        "base": {
            "50": "oklch(98.5% .002 247.839)",
            "100": "oklch(96.7% .003 264.542)",
            "200": "oklch(92.8% .006 264.531)",
            "300": "oklch(87.2% .01 258.338)",
            "400": "oklch(70.7% .022 261.325)",
            "500": "oklch(55.1% .027 264.364)",
            "600": "oklch(44.6% .03 256.802)",
            "700": "oklch(37.3% .034 259.733)",
            "800": "oklch(27.8% .033 256.848)",
            "900": "oklch(21% .034 264.665)",
            "950": "oklch(13% .028 261.692)",
        },
        # Primary color (purple by default, customize as needed)
        "primary": {
            "50": "oklch(97.7% .014 308.299)",
            "100": "oklch(94.6% .033 307.174)",
            "200": "oklch(90.2% .063 306.703)",
            "300": "oklch(82.7% .119 306.383)",
            "400": "oklch(71.4% .203 305.504)",
            "500": "oklch(62.7% .265 303.9)",
            "600": "oklch(55.8% .288 302.321)",
            "700": "oklch(49.6% .265 301.924)",
            "800": "oklch(43.8% .218 303.724)",
            "900": "oklch(38.1% .176 304.987)",
            "950": "oklch(29.1% .149 302.717)",
        },
        # Font colors (reference base colors)
        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "var(--color-base-400)",
            "default-light": "var(--color-base-600)",
            "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)",
            "important-dark": "var(--color-base-100)",
        },
    },

    # =========================================================================
    # Dashboard
    # =========================================================================
    "DASHBOARD_CALLBACK": "myapp.admin.dashboard_callback",

    # =========================================================================
    # Environment Badge
    # =========================================================================
    "ENVIRONMENT": "myapp.admin.environment_callback",
    # "ENVIRONMENT_TITLE_PREFIX": "myapp.admin.environment_title_callback",

    # =========================================================================
    # Custom CSS and JavaScript
    # =========================================================================
    "STYLES": [
        lambda request: static("css/admin-custom.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/admin-custom.js"),
    ],

    # =========================================================================
    # Sidebar Configuration
    # =========================================================================
    "SIDEBAR": {
        "show_search": True,           # Search bar in sidebar
        "command_search": False,       # Use command palette for search
        "show_all_applications": False, # Show all registered apps

        # IMPORTANT: Each entry in navigation must have an "items" list
        "navigation": [
            # Group 1: Dashboard (no section header)
            {
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            # Group 2: Content section with separator
            {
                "separator": True,
                "title": _("Content"),
                "items": [],  # Empty items for separator-only group
            },
            # Group 3: Blog (collapsible)
            {
                "title": _("Blog"),
                "icon": "article",
                "collapsible": True,
                "items": [
                    {
                        "title": _("Posts"),
                        "icon": "edit_note",
                        "link": reverse_lazy("admin:blog_post_changelist"),
                        "badge": "myapp.admin.posts_badge",  # Callback for badge
                    },
                    {
                        "title": _("Categories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:blog_category_changelist"),
                    },
                    {
                        "title": _("Tags"),
                        "icon": "label",
                        "link": reverse_lazy("admin:blog_tag_changelist"),
                    },
                ],
            },
            # Group 4: Shop (collapsible)
            {
                "title": _("Shop"),
                "icon": "shopping_cart",
                "collapsible": True,
                "items": [
                    {
                        "title": _("Products"),
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:shop_product_changelist"),
                    },
                    {
                        "title": _("Orders"),
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:shop_order_changelist"),
                        "badge": "myapp.admin.orders_badge",
                    },
                    {
                        "title": _("Customers"),
                        "icon": "people",
                        "link": reverse_lazy("admin:shop_customer_changelist"),
                    },
                ],
            },
            # Group 5: Administration separator
            {
                "separator": True,
                "title": _("Administration"),
                "items": [],
            },
            # Group 6: Users & Groups (collapsible)
            {
                "title": _("Users & Groups"),
                "icon": "admin_panel_settings",
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            # Group 7: Settings (standalone item)
            {
                "items": [
                    {
                        "title": _("Settings"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:config_settings_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },

    # =========================================================================
    # Tabs (Model-level tabs)
    # =========================================================================
    "TABS": [
        {
            "models": ["auth.user", "auth.group"],
            "items": [
                {
                    "title": _("Users"),
                    "link": reverse_lazy("admin:auth_user_changelist"),
                },
                {
                    "title": _("Groups"),
                    "link": reverse_lazy("admin:auth_group_changelist"),
                },
            ],
        },
        {
            "models": ["shop.product", "shop.category"],
            "items": [
                {
                    "title": _("Products"),
                    "link": reverse_lazy("admin:shop_product_changelist"),
                },
                {
                    "title": _("Categories"),
                    "link": reverse_lazy("admin:shop_category_changelist"),
                },
            ],
        },
    ],

    # =========================================================================
    # Login Page
    # =========================================================================
    "LOGIN": {
        "image": lambda request: static("images/login-bg.jpg"),
        "redirect_after": reverse_lazy("admin:index"),
        # "form": "myapp.forms.CustomLoginForm",  # Custom login form
    },

    # =========================================================================
    # Account Dropdown
    # =========================================================================
    "ACCOUNT": {
        "navigation": [
            {
                "title": _("Profile"),
                "icon": "person",
                "link": reverse_lazy("admin:auth_user_change", args=["__user_pk__"]),
            },
            {
                "title": _("Settings"),
                "icon": "settings",
                "link": "/admin/settings/",
            },
        ],
    },

    # =========================================================================
    # Site Dropdown (Header)
    # =========================================================================
    "SITE_DROPDOWN": [
        {
            "title": _("Main Site"),
            "icon": "home",
            "link": "/",
        },
        {
            "title": _("Documentation"),
            "icon": "description",
            "link": "/docs/",
        },
        {
            "title": _("Support"),
            "icon": "help",
            "link": "/support/",
        },
    ],

    # =========================================================================
    # Command Palette
    # =========================================================================
    "COMMAND": {
        "search_models": True,    # Enable model search
        "show_history": True,     # Show recent history
        # "search_callback": "myapp.admin.command_search_callback",
    },

    # =========================================================================
    # Extensions
    # =========================================================================
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "us",
                "es": "es",
            },
        },
    },
}


# =============================================================================
# Callback Functions (typically in myapp/admin.py)
# =============================================================================

# Dashboard callback
def dashboard_callback(request, context):
    """Add custom data to dashboard context."""
    from django.contrib.auth import get_user_model
    from shop.models import Order

    User = get_user_model()

    context.update({
        "total_users": User.objects.count(),
        "total_orders": Order.objects.count(),
        "pending_orders": Order.objects.filter(status="pending").count(),
        "recent_orders": Order.objects.order_by("-created_at")[:5],
    })
    return context


# Environment callback
def environment_callback(request):
    """Return environment badge [text, color]."""
    import os

    env = os.environ.get("DJANGO_ENV", "development")

    if env == "production":
        return None  # No badge in production
    elif env == "staging":
        return ["Staging", "warning"]
    else:
        return ["Development", "info"]


# Badge callbacks
def posts_badge(request):
    """Return draft post count for badge."""
    from blog.models import Post
    count = Post.objects.filter(status="draft").count()
    return count if count > 0 else None


def orders_badge(request):
    """Return pending order count for badge."""
    from shop.models import Order
    count = Order.objects.filter(status="pending").count()
    return count if count > 0 else None
