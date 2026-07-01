# Claude Code Skill: Django Unfold Admin

A [Claude Code](https://claude.com/claude-code) skill that provides comprehensive reference documentation and examples for building modern Django admin interfaces with [django-unfold](https://github.com/unfoldadmin/django-unfold).

## Why?

Claude Code knows Django admin well — it'll happily generate `ModelAdmin` classes, inlines, and filters that follow standard Django conventions. But django-unfold isn't standard Django admin. It has its own class hierarchy (`unfold.admin.ModelAdmin` instead of `admin.ModelAdmin`), its own action placement system with four distinct decorator locations, its own Tailwind-based component styling, OKLch color configuration, and a suite of advanced filter types that don't exist in vanilla Django.

Without guidance, Claude Code will fall back to what it knows: standard Django patterns, generic Tailwind classes, and Bootstrap-style markup. The result looks wrong — mismatched styling, missing dark mode support, actions in the wrong places, and filters that don't use Unfold's enhanced types.

This skill fixes that. It gives Claude Code the exact class names, component patterns, decorator signatures, and HTML structures that Unfold expects, so the code it generates actually works with the framework rather than fighting it.

## What Is This?

A [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code/skills) — a structured knowledge pack that Claude Code loads automatically when you ask it to build or modify Django admin pages using django-unfold. It contains reference documentation and examples that guide Claude Code to produce correct, well-styled admin interfaces using the right Tailwind classes, component patterns, and API conventions.

This skill is not affiliated with the django-unfold project. It is an independently maintained reference guide built from the public documentation and source code.

## Installation

This skill ships as a Claude Code **plugin** (`rwts-unfold-admin`), distributed via the RWTS Claude Code marketplace. Add the marketplace once, then install the plugin:

```bash
/plugin marketplace add git@github.realworld.net.au:realworldtech/claude-marketplace.git
/plugin install rwts-unfold-admin@rwts
```

Claude Code will automatically detect and use the skill when you ask about Django admin, unfold, admin actions, admin filters, or admin theming.

### Updating

```bash
/plugin marketplace update rwts
```

### Uninstalling

```bash
/plugin uninstall rwts-unfold-admin@rwts
```

## What It Covers

- **Actions and decorators** — `@action` placement options, confirmation/form dialogs, `@display` decorator for list views, permission handling
- **Filters and search** — Dropdown, radio/checkbox, date/time, numeric, text, autocomplete, facet, and horizontal filters
- **Inlines and sections** — TabularInline, StackedInline, nested & paginated inlines, `InfinitePaginator`, sections, datasets, conditional fields, sortable changelist
- **Settings and configuration** — UNFOLD settings dictionary, branding, colors (OKLCH), sidebar navigation, command palette, tabs, dashboard
- **Components** — Unfold's `{% component %}` library: cards, buttons, progress, trackers, tables, and Chart.js charts
- **Templates and styling** — HTML template patterns, Tailwind 4, Material Symbols icons, dark mode, form widgets, CSS class constants
- **Integrations** — celery-beat/results, simple-history, modeltranslation, import-export, hijack, djangoql, constance, guardian, location-field, money

## Usage

Once installed, just ask Claude Code to work on Django admin. The skill triggers automatically. For example:

- "Create a Django admin for my Product model with filters and actions"
- "Add a custom dashboard page to my unfold admin"
- "Style my admin with unfold"
- "Add row-level actions to my OrderAdmin"

## Structure

```
.claude-plugin/
  plugin.json                          # Plugin manifest (marketplace metadata)
skills/
  unfold-admin/
    SKILL.md                           # Main skill definition and quick-start guide
    examples/
      user-admin.py                    # User & Group admin (default, AbstractUser, AbstractBaseUser)
      basic-admin.py                   # Simple ModelAdmin patterns
      third-party-admin.py             # Fixing celery-beat, celery-results, hijack, djangoql, etc.
      advanced-admin.py                # Full-featured admin (actions incl. dialogs, filters, inlines, conditional fields)
      settings-example.py              # Complete UNFOLD settings configuration
      custom-dashboard.html            # Dashboard using the {% component %} library + Tailwind
    references/
      actions-and-decorators.md        # @action (incl. dialogs) and @display decorator reference
      filters-and-search.md            # Filter types, facet/horizontal filters, search
      inlines-and-sections.md          # Inlines (nested/paginated), sections, datasets, conditional fields, sortable
      settings-configuration.md        # UNFOLD settings dict, sidebar, command palette, dashboard
      templates-and-components.md      # HTML templates, Tailwind 4, Material Symbols, dark mode
      components.md                    # Unfold's {% component %} library (cards, charts, tables, buttons, etc.)
      widgets-and-styling.md           # Widget reference and CSS class constants
      integrations.md                  # Third-party packages (celery, hijack, djangoql, import-export, etc.)
```

Targets **django-unfold 0.97.x** (Django ≥ 5.2, Python ≥ 3.12).

## Upstream

- **Package:** [django-unfold](https://github.com/unfoldadmin/django-unfold) (MIT license)
- **Documentation:** [unfoldadmin.com](https://unfoldadmin.com)
- **PyPI:** `pip install django-unfold`

## License

MIT
