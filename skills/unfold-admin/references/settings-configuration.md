# UNFOLD Settings Configuration

Complete reference for the `UNFOLD` dictionary in Django settings.

## Basic Structure

**Key gotcha:** branding assets (`SITE_ICON`, `SITE_LOGO`, `SITE_FAVICONS` href), `STYLES`/`SCRIPTS`, and `LOGIN` images are **callables** `lambda request: static("...")` — not plain path strings. Use `django.templatetags.static.static` (importable as `from django.templatetags.static import static`).

```python
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    # Site branding
    "SITE_TITLE": "My Admin",
    "SITE_HEADER": "My Admin Panel",
    "SITE_SUBHEADER": "Management Dashboard",
    "SITE_URL": "/",

    # Site icon / logo (callables; can be a single callable or a light/dark dict of callables)
    "SITE_ICON": lambda request: static("icon.svg"),
    "SITE_SYMBOL": "speed",            # Material Symbol name (alternative to an icon image)
    "SITE_LOGO": {
        "light": lambda request: static("logo-light.svg"),
        "dark": lambda request: static("logo-dark.svg"),
    },

    # Favicons — href is a callable
    "SITE_FAVICONS": [
        {"rel": "icon", "sizes": "32x32", "type": "image/png",
         "href": lambda request: static("favicon-32x32.png")},
    ],

    # Feature toggles
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": False,
    "SHOW_UI_WARNINGS": False,         # show/hide Unfold's UI warnings

    # Forced theme + radius
    "THEME": None,                     # "dark" or "light" forces a theme AND hides the switcher
    "BORDER_RADIUS": "6px",

    # Language settings
    "SHOW_LANGUAGES": False,
    "LANGUAGE_FLAGS": {"en": "us", "de": "de", "fr": "fr"},

    # Colors (OKLCH system) — see below
    "COLORS": {...},

    # Callbacks (dotted import-string paths)
    "DASHBOARD_CALLBACK": "myapp.admin.dashboard_callback",   # dashboard context
    "GLOBAL_CALLBACK": "myapp.admin.global_callback",         # context merged into EVERY admin page
    "ENVIRONMENT": "myapp.admin.environment_callback",
    "ENVIRONMENT_TITLE_PREFIX": "myapp.admin.environment_title_callback",

    # Custom CSS/JS (lists of callables)
    "STYLES": [lambda request: static("admin/custom.css")],
    "SCRIPTS": [lambda request: static("admin/custom.js")],

    # Form field class overrides (advanced)
    "FORMS": {"classes": {}},

    # Sidebar / tabs / login / dropdowns / command palette / extensions
    "SIDEBAR": {...},
    "TABS": [...],
    "LOGIN": {...},
    "ACCOUNT": {...},
    "COMMAND": {...},
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

The `SIDEBAR` dict has exactly three keys: `show_search`, `show_all_applications`, and `navigation`. (There is no `command_search` key — that was never part of Unfold.)

```python
"SIDEBAR": {
    "show_search": False,            # Search box over application/model names
    "show_all_applications": False,  # "All applications" dropdown
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
| `badge` | str/callable | No | Group-level badge (int/str or import-string callback) |
| `permission` | callable/str | No | Hide the whole group (`lambda request: bool` or import-string) |

### Navigation Item Properties (inside `items`)

| Property | Type | Description |
|----------|------|-------------|
| `title` | str | Display text |
| `icon` | str | **Material Symbol name - PUT ICON HERE** |
| `link` | str/callable | URL path, reverse_lazy, or lambda |
| `badge` | int/str/callable | Badge value, or import-string callback `cb(request) -> int\|str` |
| `badge_variant` | str | `info` / `success` / `warning` / `primary` / `danger` |
| `badge_style` | str | Badge fill style, e.g. `"solid"` |
| `permission` | callable/str | `lambda request: bool` or import-string |
| `active` | bool/callable | Force active state (auto-detected if omitted) |
| `items` | list | Nested sub-items (for nested menus) |

## Tabs Configuration

`TABS` is a list of dicts (or a dotted import-string for dynamic tabs). Each entry binds tab `items` to one or more models.

**Changelist tabs** — `models` entries are plain `app_label.model` strings:

```python
"TABS": [
    {
        "models": ["auth.user", "auth.group"],
        "items": [
            {"title": "Users", "link": reverse_lazy("admin:auth_user_changelist")},
            {"title": "Groups", "link": reverse_lazy("admin:auth_group_changelist"),
             "permission": "myapp.admin.tabs_permission_callback"},
        ],
    },
]
```

**Changeform (detail) tabs** — each `models` entry is a dict with `detail: True`:

```python
"TABS": [
    {
        "models": [{"name": "auth.user", "detail": True}],
        "items": [
            {"title": "Profile", "link": reverse_lazy("admin:auth_user_change", args=["__pk__"])},
        ],
    },
]
```

Item keys: `title`, `link`, `permission` (callable/import-string), `active` (bool/callable). For fully dynamic tabs, set `"TABS": "myapp.admin.tabs_callback"` where the callback returns the same list shape.

## Login Configuration

`image` and `redirect_after` are **callables**; `form` is a dotted import-string for a custom auth form (which must subclass `unfold.forms.AuthenticationForm`).

```python
"LOGIN": {
    "image": lambda request: static("admin/login-bg.jpg"),
    "redirect_after": lambda request: reverse_lazy("admin:index"),
    "form": "myapp.forms.CustomLoginForm",
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

The command palette opens with **⌘K / Ctrl-K**. Configure it under `COMMAND` (three keys).

```python
"COMMAND": {
    "search_models": False,   # see options below
    "show_history": False,    # remember recent queries (stored client-side in localStorage)
    "search_callback": "myapp.admin.command_search_callback",  # inject custom results
}
```

`search_models` accepts:
- `False` (default) / `True` — `True` searches every admin model that defines `search_fields`.
- a list of model strings, e.g. `["shop.order", "shop.product"]` — allow-list.
- a dotted import-string callback `cb(request) -> list[str]` returning allowed model strings.

A model is only searchable if its `ModelAdmin` defines `search_fields`. Searching all models is DB-intensive; results use infinite scrolling (page size 100).

`search_callback` is a dotted import-string for a custom result hook. It must return a list of `SearchResult` objects, and you handle permissions yourself:

```python
# myapp/admin.py
from unfold.dataclasses import SearchResult

def command_search_callback(request, search_term):
    results = []
    for order in Order.objects.filter(reference__icontains=search_term)[:20]:
        results.append(SearchResult(
            title=order.reference,
            description=f"Order for {order.customer}",
            link=reverse("admin:shop_order_change", args=[order.pk]),
            icon="receipt_long",   # optional Material Symbol
        ))
    return results
```

> `SearchResult` takes **keyword arguments** (`title`, `description`, `link`, `icon`). The official docs show a dict-style call (`SearchResult("title": ...)`) which is invalid Python — use keywords.

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

`DASHBOARD_CALLBACK` only feeds the dashboard (`admin/index.html`). To inject context into **every** admin page, use `GLOBAL_CALLBACK` (a dotted import-string), whose callable takes just `request` and returns a dict:

```python
# settings.py
"GLOBAL_CALLBACK": "myapp.admin.global_callback"

# myapp/admin.py
def global_callback(request):
    return {"support_url": "https://support.example.com"}
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
            "en": "🇬🇧",
            "de": "🇩🇪",
            "fr": "🇫🇷",
        },
    },
}
```
