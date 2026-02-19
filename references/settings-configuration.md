# UNFOLD Settings Configuration

Complete reference for the `UNFOLD` dictionary in Django settings.

## Basic Structure

```python
UNFOLD = {
    # Site branding
    "SITE_TITLE": "My Admin",
    "SITE_HEADER": "My Admin Panel",
    "SITE_SUBHEADER": "Management Dashboard",
    "SITE_URL": "/",

    # Site icon options (choose one)
    "SITE_ICON": "/static/icon.svg",  # Path to icon file
    "SITE_SYMBOL": "dashboard",        # Material Symbol name
    "SITE_LOGO": {                     # Logo with light/dark variants
        "light": {"url": "/static/logo-light.svg", "alt": "Logo"},
        "dark": {"url": "/static/logo-dark.svg", "alt": "Logo"},
    },

    # Favicons
    "SITE_FAVICONS": [
        {"rel": "icon", "sizes": "32x32", "type": "image/png", "href": "/static/favicon-32x32.png"},
        {"rel": "icon", "sizes": "16x16", "type": "image/png", "href": "/static/favicon-16x16.png"},
        {"rel": "apple-touch-icon", "sizes": "180x180", "href": "/static/apple-touch-icon.png"},
    ],

    # Feature toggles
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": False,

    # Language settings
    "SHOW_LANGUAGES": False,
    "LANGUAGE_FLAGS": {
        "en": "us",
        "de": "de",
        "fr": "fr",
    },

    # Colors (OKLch system)
    "COLORS": {...},

    # Dashboard
    "DASHBOARD_CALLBACK": "myapp.admin.dashboard_callback",

    # Environment badge
    "ENVIRONMENT": "myapp.admin.environment_callback",
    "ENVIRONMENT_TITLE_PREFIX": "myapp.admin.environment_title_callback",

    # Custom CSS/JS
    "STYLES": ["/static/admin/custom.css"],
    "SCRIPTS": ["/static/admin/custom.js"],

    # Sidebar
    "SIDEBAR": {...},

    # Tabs
    "TABS": [...],

    # Login
    "LOGIN": {...},

    # Account dropdown
    "ACCOUNT": {...},

    # Command palette
    "COMMAND": {...},

    # Extensions
    "EXTENSIONS": {...},
}
```

## Color Configuration

Colors use the OKLch color space. Define shades 50-950:

```python
"COLORS": {
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
    "font": {
        "subtle-light": "var(--color-base-500)",
        "subtle-dark": "var(--color-base-400)",
        "default-light": "var(--color-base-600)",
        "default-dark": "var(--color-base-300)",
        "important-light": "var(--color-base-900)",
        "important-dark": "var(--color-base-100)",
    },
}
```

## Sidebar Configuration

**IMPORTANT:** Navigation items must be wrapped in groups with an `items` key.

```python
"SIDEBAR": {
    "show_search": False,      # Search bar in sidebar
    "command_search": False,   # Open command palette from search
    "show_all_applications": False,  # Show all registered apps
    "navigation": [
        # Group 1: Simple items (no section header)
        {
            "items": [
                {
                    "title": "Dashboard",
                    "icon": "dashboard",
                    "link": reverse_lazy("admin:index"),
                },
            ],
        },
        # Group 2: Collapsible section with header
        {
            "title": "Users & Groups",
            "icon": "people",
            "collapsible": True,
            "items": [
                {
                    "title": "Users",
                    "icon": "person",
                    "link": reverse_lazy("admin:auth_user_changelist"),
                    "badge": "myapp.admin.users_badge_callback",
                    "permission": lambda request: request.user.is_superuser,
                },
                {
                    "title": "Groups",
                    "icon": "group",
                    "link": reverse_lazy("admin:auth_group_changelist"),
                },
            ],
        },
        # Group 3: Separator with section title
        {
            "separator": True,
            "title": "Content",
            "items": [
                {
                    "title": "Articles",
                    "icon": "article",
                    "link": reverse_lazy("admin:blog_article_changelist"),
                },
            ],
        },
    ],
}
```

### Navigation Structure

Each entry in `navigation` is a **group** that MUST have an `items` list:

```python
# Simple group (no header) - icons go on ITEMS
{
    "items": [
        {
            "title": "Dashboard",
            "icon": "dashboard",      # <-- Icon on each item
            "link": reverse_lazy("admin:index"),
        },
    ],
}

# Collapsible group - icon on GROUP (for header), AND on each ITEM
{
    "title": "Users & Groups",
    "icon": "people",                 # <-- Icon on collapsible header
    "collapsible": True,
    "items": [
        {
            "title": "Users",
            "icon": "person",         # <-- Icon on each item too
            "link": reverse_lazy("admin:auth_user_changelist"),
        },
    ],
}
```

### Where Icons Go

| Group Type | Icon Location |
|------------|---------------|
| Simple group (no header) | **Items only** - group icon is ignored |
| Collapsible group | **Group AND items** - group icon shows in header |
| Separator | No icon needed |

### Navigation Group Properties (top-level entries)

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `items` | list | **YES** | List of navigation items (see below) |
| `title` | str | No | Section header text (for collapsible/separator) |
| `icon` | str | No | Icon for collapsible header ONLY |
| `collapsible` | bool | No | Group can collapse/expand |
| `separator` | bool | No | Render as visual separator |

### Navigation Item Properties (inside `items`)

| Property | Type | Description |
|----------|------|-------------|
| `title` | str | Display text |
| `icon` | str | **Material Symbol name - PUT ICON HERE** |
| `link` | str/callable | URL path, reverse_lazy, or lambda |
| `badge` | str/callable | Badge callback path or callable |
| `permission` | callable | `lambda request: bool` |
| `items` | list | Nested sub-items (for nested menus) |

## Tabs Configuration

Add tabs above content on specific pages:

```python
"TABS": [
    {
        "models": ["auth.user", "auth.group"],
        "items": [
            {"title": "Users", "link": reverse_lazy("admin:auth_user_changelist")},
            {"title": "Groups", "link": reverse_lazy("admin:auth_group_changelist")},
        ],
    },
]
```

## Login Configuration

```python
"LOGIN": {
    "image": "/static/admin/login-bg.jpg",  # Background image
    "redirect_after": "/admin/",             # Post-login redirect
    "form": "myapp.forms.CustomLoginForm",   # Custom form class
}
```

## Account Dropdown

```python
"ACCOUNT": {
    "navigation": [
        {
            "title": "Profile",
            "icon": "person",
            "link": reverse_lazy("admin:profile"),
        },
        {
            "title": "Settings",
            "icon": "settings",
            "link": "/admin/settings/",
        },
    ],
}
```

## Command Palette

```python
"COMMAND": {
    "search_models": False,   # Include models in search
    "show_history": False,    # Show recent history
    "search_callback": "myapp.admin.command_search_callback",
}
```

## Site Dropdown

Custom dropdown menu in header:

```python
"SITE_DROPDOWN": [
    {
        "title": "Main Site",
        "icon": "home",
        "link": "/",
    },
    {
        "title": "Documentation",
        "icon": "description",
        "link": "/docs/",
    },
],
```

## Dashboard Callback

```python
# settings.py
"DASHBOARD_CALLBACK": "myapp.admin.dashboard_callback"

# myapp/admin.py
def dashboard_callback(request, context):
    context.update({
        "cards": [
            {"title": "Users", "value": User.objects.count()},
            {"title": "Orders", "value": Order.objects.count()},
        ],
    })
    return context
```

## Environment Badge

Display environment indicator:

```python
# settings.py
"ENVIRONMENT": "myapp.admin.environment_callback"

# myapp/admin.py
def environment_callback(request):
    return ["Development", "warning"]  # [text, color: warning/danger/success]
```

## Extensions

Configure extension-specific settings:

```python
"EXTENSIONS": {
    "modeltranslation": {
        "flags": {
            "en": "us",
            "de": "de",
        },
    },
}
```
