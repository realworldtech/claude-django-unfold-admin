# Templates and Components Reference

## CRITICAL: Color System

Unfold uses TWO types of colors:

### Themeable Colors (from UNFOLD settings)
These respect the `COLORS` configuration in `settings.py`:
- **`primary-{50-950}`** - Accent/brand color (buttons, links, focus states)
- **`base-{50-950}`** - Neutral gray scale (backgrounds, borders, text)

```html
<!-- These use the theme's configured colors -->
<button class="bg-primary-600 text-white">Themed Button</button>
<div class="bg-base-100 text-base-900 dark:bg-base-800 dark:text-base-100">Card</div>
```

### Fixed Semantic Colors (standard Tailwind)
These are NOT configurable - use for semantic meaning:
- **`red-{50-950}`** - Danger, errors, delete actions
- **`green-{50-950}`** - Success, active states
- **`yellow-{50-950}`** - Warnings, pending states
- **`blue-{50-950}`** - Info, informational messages

```html
<!-- These are fixed Tailwind colors -->
<span class="bg-red-100 text-red-800">Error</span>
<span class="bg-green-100 text-green-800">Success</span>
```

### When to Use Each
| Purpose | Use |
|---------|-----|
| Primary buttons, links, focus rings | `primary-*` (themed) |
| Backgrounds, borders, neutral text | `base-*` (themed) |
| Delete/error/danger states | `red-*` (fixed) |
| Success/active/confirmed states | `green-*` (fixed) |
| Warning/pending states | `yellow-*` (fixed) |
| Info/help messages | `blue-*` (fixed) |

## Template Customization

### Extending Base Templates

Unfold provides customizable template blocks:

```html
{% extends "admin/base_site.html" %}

{% block extrahead %}
    {{ block.super }}
    <link rel="stylesheet" href="{% static 'css/custom.css' %}">
{% endblock %}

{% block extrastyle %}
    {{ block.super }}
    <style>
        /* Custom styles */
    </style>
{% endblock %}
```

### Dashboard Template

Create a custom dashboard by setting `DASHBOARD_CALLBACK`:

```python
# settings.py
UNFOLD = {
    "DASHBOARD_CALLBACK": "myapp.admin.dashboard_callback",
}

# myapp/admin.py
def dashboard_callback(request, context):
    context.update({
        "stats": [
            {"title": "Users", "value": User.objects.count(), "icon": "person"},
            {"title": "Orders", "value": Order.objects.count(), "icon": "shopping_cart"},
        ],
        "recent_orders": Order.objects.order_by("-created_at")[:5],
    })
    return context
```

Then override the index template:

```html
<!-- templates/admin/index.html -->
{% extends "admin/index.html" %}
{% load i18n unfold %}

{% block content %}
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
    {% for stat in stats %}
    <div class="bg-white dark:bg-base-900 rounded-default p-4 shadow-sm">
        <div class="flex items-center">
            <span class="material-symbols-outlined text-primary-600 mr-3">
                {{ stat.icon }}
            </span>
            <div>
                <div class="text-2xl font-bold">{{ stat.value }}</div>
                <div class="text-sm text-base-500">{{ stat.title }}</div>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{{ block.super }}
{% endblock %}
```

## ModelAdmin Template Hooks

### Changelist Templates

```python
class MyModelAdmin(ModelAdmin):
    list_before_template = "admin/myapp/mymodel/list_before.html"
    list_after_template = "admin/myapp/mymodel/list_after.html"
```

### Change Form Templates

```python
class MyModelAdmin(ModelAdmin):
    change_form_before_template = "admin/myapp/mymodel/change_form_before.html"
    change_form_after_template = "admin/myapp/mymodel/change_form_after.html"
    change_form_outer_before_template = "admin/myapp/mymodel/outer_before.html"
    change_form_outer_after_template = "admin/myapp/mymodel/outer_after.html"
```

Template placement:
- `outer_before` - Before the entire form container
- `before` - Inside form container, before fieldsets
- `after` - Inside form container, after fieldsets
- `outer_after` - After the entire form container

## Object Action Buttons (Change Form Header)

**CRITICAL:** For adding buttons to the change form header (the area with History/View on site), there are two approaches:

### Recommended: Use `actions_detail` in Python

The preferred approach is to use `actions_detail` with the `@action` decorator. This automatically handles styling, permissions, and URLs correctly. See `references/actions-and-decorators.md` for details.

```python
from unfold.decorators import action

class MyModelAdmin(ModelAdmin):
    actions_detail = ["my_custom_action"]

    @action(description="My Action", icon="add_circle", url_path="my-action")
    def my_custom_action(self, request, object_id):
        # Handle the action
        return redirect(...)
```

### Template Override: Use the Correct Include

If you MUST add buttons via template override (e.g., for links to external pages), you MUST use the `tab_action.html` template include. **DO NOT write raw HTML `<li><a>` elements.**

Create a custom change_form.html template:

```html
<!-- templates/admin/myapp/mymodel/change_form.html -->
{% extends "admin/change_form.html" %}
{% load i18n admin_urls %}

{% block object-tools-items %}
    {{ block.super }}

    {# CORRECT: Use the tab_action.html include #}
    {% include "unfold/helpers/tab_action.html" with title="New Campaign Wizard" link="/admin/support/bulkemailcampaign/wizard/new/" icon="add_circle" %}
{% endblock %}
```

**WRONG - Do NOT do this:**
```html
{# WRONG: Raw HTML will not have correct Unfold styling #}
<li>
    <a href="/admin/some/url/" class="inline-flex items-center gap-2">
        <span class="material-symbols-outlined text-lg">add_circle</span>
        My Action
    </a>
</li>
```

**CORRECT - Use template include:**
```html
{# CORRECT: Uses Unfold's styling system #}
{% include "unfold/helpers/tab_action.html" with title="My Action" link="/admin/some/url/" icon="add_circle" %}
```

### tab_action.html Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `title` | str | Button text (required) |
| `link` | str | URL for the button (required for links) |
| `icon` | str | Material Symbol icon name |
| `blank` | bool | If true, opens in new tab (target="_blank") |
| `action` | dict | Action object (for dropdown actions, advanced use) |

### Examples

Simple link button:
```html
{% include "unfold/helpers/tab_action.html" with title="View Report" link="/admin/reports/view/" icon="description" %}
```

External link (opens in new tab):
```html
{% include "unfold/helpers/tab_action.html" with title="External Docs" link="https://docs.example.com" icon="open_in_new" blank=1 %}
```

Dynamic URL with object ID:
```html
{% url 'admin:myapp_mymodel_custom' original.pk as custom_url %}
{% include "unfold/helpers/tab_action.html" with title="Custom Action" link=custom_url icon="bolt" %}
```

### Full Example: Custom Wizard View with URL

Here's a complete example of adding a wizard button that links to a custom view:

**1. Define the custom view and URL in your ModelAdmin:**

```python
# admin.py
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path, reverse
from unfold.admin import ModelAdmin

@admin.register(BulkEmailCampaign)
class BulkEmailCampaignAdmin(ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "wizard/new/",
                self.admin_site.admin_view(self.wizard_view),
                name="support_bulkemailcampaign_wizard",
            ),
        ]
        return custom_urls + urls

    def wizard_view(self, request):
        # Your wizard logic here
        context = {
            **self.admin_site.each_context(request),
            "title": "New Campaign Wizard",
            "opts": self.model._meta,
        }
        return render(request, "admin/support/bulkemailcampaign/wizard.html", context)
```

**2. Create the template override to add the button:**

```html
<!-- templates/admin/support/bulkemailcampaign/change_form.html -->
{% extends "admin/change_form.html" %}
{% load i18n admin_urls %}

{% block object-tools-items %}
    {{ block.super }}

    {% url 'admin:support_bulkemailcampaign_wizard' as wizard_url %}
    {% include "unfold/helpers/tab_action.html" with title="New Campaign Wizard" link=wizard_url icon="add_circle" %}
{% endblock %}
```

**3. Create the wizard template (optional, for the wizard page itself):**

```html
<!-- templates/admin/support/bulkemailcampaign/wizard.html -->
{% extends "admin/base_site.html" %}
{% load i18n unfold %}

{% block content %}
<div class="bg-white dark:bg-base-900 rounded-default shadow-sm p-6">
    <h2 class="text-xl font-semibold text-base-900 dark:text-base-100 mb-4">
        Campaign Wizard
    </h2>
    <!-- Your wizard form/content here -->
</div>
{% endblock %}
```

## Component Classes

### Cards

```html
<div class="bg-white dark:bg-base-900 rounded-default shadow-sm p-4">
    <h3 class="text-lg font-semibold text-base-900 dark:text-base-100 mb-2">
        Card Title
    </h3>
    <p class="text-base-600 dark:text-base-400">
        Card content goes here.
    </p>
</div>
```

### Stat Cards

```html
<div class="bg-white dark:bg-base-900 rounded-default shadow-sm p-4">
    <div class="flex items-center justify-between">
        <div>
            <div class="text-sm text-base-500 dark:text-base-400">Total Users</div>
            <div class="text-2xl font-bold text-base-900 dark:text-base-100">
                {{ user_count }}
            </div>
        </div>
        <div class="bg-primary-100 dark:bg-primary-900 p-3 rounded-full">
            <span class="material-symbols-outlined text-primary-600">person</span>
        </div>
    </div>
</div>
```

### Tables

```html
<div class="overflow-x-auto">
    <table class="w-full">
        <thead>
            <tr class="border-b border-base-200 dark:border-base-700">
                <th class="px-4 py-3 text-left text-sm font-semibold
                           text-base-900 dark:text-base-100">
                    Header
                </th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr class="border-b border-base-100 dark:border-base-800
                       hover:bg-base-50 dark:hover:bg-base-800">
                <td class="px-4 py-3 text-sm text-base-600 dark:text-base-400">
                    {{ item.name }}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
```

### Badges/Labels

**Themed badge** (uses configured primary color):
```html
<span class="inline-flex items-center px-2 py-1 rounded-default text-xs
             font-medium bg-primary-100 text-primary-800
             dark:bg-primary-900 dark:text-primary-200">
    Default
</span>
```

**Semantic badges** (fixed colors for specific meanings):
```html
<!-- Success (green) - for active/confirmed states -->
<span class="inline-flex items-center px-2 py-1 rounded-default text-xs
             font-medium bg-green-100 text-green-800
             dark:bg-green-900/30 dark:text-green-300">
    Active
</span>

<!-- Warning (yellow) - for pending/attention states -->
<span class="inline-flex items-center px-2 py-1 rounded-default text-xs
             font-medium bg-yellow-100 text-yellow-800
             dark:bg-yellow-900/30 dark:text-yellow-300">
    Pending
</span>

<!-- Danger (red) - for errors/deleted/expired states -->
<span class="inline-flex items-center px-2 py-1 rounded-default text-xs
             font-medium bg-red-100 text-red-800
             dark:bg-red-900/30 dark:text-red-300">
    Expired
</span>

<!-- Info (blue) - for informational states -->
<span class="inline-flex items-center px-2 py-1 rounded-default text-xs
             font-medium bg-blue-100 text-blue-800
             dark:bg-blue-900/30 dark:text-blue-300">
    New
</span>

<!-- Neutral (base) - for inactive/default states -->
<span class="inline-flex items-center px-2 py-1 rounded-default text-xs
             font-medium bg-base-100 text-base-700
             dark:bg-base-800 dark:text-base-300">
    Draft
</span>
```

### Buttons

```html
<!-- Primary -->
<button class="px-4 py-2 bg-primary-600 text-white rounded-default
               font-medium hover:bg-primary-700 transition-colors">
    Primary Action
</button>

<!-- Secondary -->
<button class="px-4 py-2 bg-base-100 text-base-700 rounded-default
               font-medium hover:bg-base-200 transition-colors
               dark:bg-base-800 dark:text-base-200 dark:hover:bg-base-700">
    Secondary
</button>

<!-- Danger -->
<button class="px-4 py-2 bg-red-600 text-white rounded-default
               font-medium hover:bg-red-700 transition-colors">
    Delete
</button>

<!-- Ghost -->
<button class="px-4 py-2 text-primary-600 rounded-default
               font-medium hover:bg-primary-50 transition-colors
               dark:hover:bg-primary-900">
    Link Style
</button>
```

### Form Elements

```html
<!-- Input -->
<input type="text"
       class="w-full px-3 py-2 border border-base-200 rounded-default
              bg-white text-base-900 text-sm
              focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600
              dark:bg-base-900 dark:border-base-700 dark:text-base-100">

<!-- Select -->
<select class="w-full px-3 py-2 border border-base-200 rounded-default
               bg-white text-base-900 text-sm appearance-none
               dark:bg-base-900 dark:border-base-700 dark:text-base-100">
    <option>Option 1</option>
    <option>Option 2</option>
</select>

<!-- Checkbox -->
<input type="checkbox"
       class="h-4 w-4 rounded border-base-300 text-primary-600
              focus:ring-primary-500 dark:border-base-600 dark:bg-base-700">

<!-- Label -->
<label class="block text-sm font-medium text-base-900 dark:text-base-100 mb-1">
    Field Label
</label>
```

### Alerts/Messages

Alerts use **semantic colors** (fixed) because they convey specific meaning:

```html
<!-- Success (green) -->
<div class="p-4 rounded-default bg-green-50 border border-green-200
            dark:bg-green-900/20 dark:border-green-800">
    <div class="flex items-center">
        <span class="material-symbols-outlined text-green-600 mr-2">check_circle</span>
        <span class="text-green-800 dark:text-green-200">Success message</span>
    </div>
</div>

<!-- Error (red) -->
<div class="p-4 rounded-default bg-red-50 border border-red-200
            dark:bg-red-900/20 dark:border-red-800">
    <div class="flex items-center">
        <span class="material-symbols-outlined text-red-600 mr-2">error</span>
        <span class="text-red-800 dark:text-red-200">Error message</span>
    </div>
</div>

<!-- Warning (yellow) -->
<div class="p-4 rounded-default bg-yellow-50 border border-yellow-200
            dark:bg-yellow-900/20 dark:border-yellow-800">
    <div class="flex items-center">
        <span class="material-symbols-outlined text-yellow-600 mr-2">warning</span>
        <span class="text-yellow-800 dark:text-yellow-200">Warning message</span>
    </div>
</div>

<!-- Info (blue) -->
<div class="p-4 rounded-default bg-blue-50 border border-blue-200
            dark:bg-blue-900/20 dark:border-blue-800">
    <div class="flex items-center">
        <span class="material-symbols-outlined text-blue-600 mr-2">info</span>
        <span class="text-blue-800 dark:text-blue-200">Info message</span>
    </div>
</div>

<!-- Neutral (base - themed) - for general notices -->
<div class="p-4 rounded-default bg-base-50 border border-base-200
            dark:bg-base-800 dark:border-base-700">
    <div class="flex items-center">
        <span class="material-symbols-outlined text-base-500 mr-2">info</span>
        <span class="text-base-700 dark:text-base-300">General notice</span>
    </div>
</div>
```

## Icons Reference

**IMPORTANT:** Unfold uses **Material Symbols**, NOT Material Icons. They have different names!

Browse icons at: https://fonts.google.com/icons?icon.set=Material+Symbols

### Common Naming Differences

| What you want | WRONG (Material Icons) | CORRECT (Material Symbols) |
|---------------|------------------------|---------------------------|
| Services | `miscellaneous_services` | `handyman` or `build` |
| Money | `attach_money` | `payments` or `currency_exchange` |
| List | `format_list_bulleted` | `list` |
| Add circle | `add_circle` | `add_circle` (same) |
| Settings | `settings` | `settings` (same) |

### Navigation
`home`, `dashboard`, `menu`, `arrow_back`, `arrow_forward`, `chevron_left`, `chevron_right`, `expand_more`, `expand_less`

### Actions
`add`, `edit`, `delete`, `save`, `close`, `check`, `refresh`, `search`, `filter_list`, `sort`, `more_vert`, `more_horiz`

### Content
`article`, `description`, `folder`, `image`, `attachment`, `link`, `draft`, `note`, `text_snippet`

### Users
`person`, `people`, `group`, `admin_panel_settings`, `account_circle`, `manage_accounts`, `badge`

### Status
`check_circle`, `cancel`, `error`, `warning`, `info`, `help`, `pending`, `verified`

### Files
`upload`, `download`, `cloud_upload`, `cloud_download`, `attach_file`, `file_upload`, `folder_open`

### Communication
`email`, `mail`, `notifications`, `chat`, `forum`, `send`, `inbox`

### E-commerce
`shopping_cart`, `payments`, `receipt`, `inventory`, `storefront`, `local_shipping`, `receipt_long`

### Business
`business`, `work`, `corporate_fare`, `domain`, `analytics`, `monitoring`, `trending_up`

### Services/Tools
`build`, `handyman`, `construction`, `engineering`, `settings`, `tune`, `support`

### Misc
`visibility`, `visibility_off`, `lock`, `lock_open`, `schedule`, `calendar_today`, `event`, `category`, `label`, `bookmark`

### Verify Icons Exist

If an icon doesn't render, search for it at:
https://fonts.google.com/icons?icon.set=Material+Symbols&icon.query=YOUR_SEARCH

## Tailwind Utilities

### Spacing
`p-{0-12}`, `px-{n}`, `py-{n}`, `m-{n}`, `mx-{n}`, `my-{n}`

### Layout
`flex`, `grid`, `grid-cols-{1-12}`, `gap-{n}`, `items-center`, `justify-between`

### Sizing
`w-full`, `w-{n}`, `max-w-{size}`, `h-{n}`, `min-h-{n}`

### Typography
`text-{xs|sm|base|lg|xl|2xl}`, `font-{normal|medium|semibold|bold}`, `text-{color}`

### Borders
`border`, `border-{n}`, `rounded-default`, `rounded-full`, `border-{color}`

### Shadows
`shadow-xs`, `shadow-sm`, `shadow`, `shadow-md`, `shadow-lg`

### Transitions
`transition`, `transition-colors`, `transition-all`, `duration-{n}`

### Dark Mode
Prefix with `dark:` for dark mode variants:
```html
<div class="bg-white dark:bg-base-900 text-base-900 dark:text-base-100">
```

## Color Reference Summary

### Themeable (from UNFOLD settings)
```
primary-{50,100,200,300,400,500,600,700,800,900,950}  - Brand/accent
base-{50,100,200,300,400,500,600,700,800,900,950}     - Neutrals
```

### Fixed Semantic (standard Tailwind)
```
red-*     - Danger, errors, delete
green-*   - Success, active, confirmed
yellow-*  - Warning, pending, attention
blue-*    - Info, informational
```

### Common Patterns
```html
<!-- Primary action -->
bg-primary-600 text-white hover:bg-primary-700

<!-- Secondary action -->
bg-base-100 text-base-700 hover:bg-base-200 dark:bg-base-800 dark:text-base-200

<!-- Danger action -->
bg-red-600 text-white hover:bg-red-700 dark:bg-red-500/20 dark:text-red-500

<!-- Card background -->
bg-white dark:bg-base-900

<!-- Border -->
border-base-200 dark:border-base-700

<!-- Text -->
text-base-900 dark:text-base-100      (primary text)
text-base-600 dark:text-base-400      (secondary text)
text-base-500 dark:text-base-500      (muted text)
```
