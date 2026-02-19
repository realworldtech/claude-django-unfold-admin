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

Clone this repository into your Claude Code skills directory:

```bash
git clone https://github.com/realworldtech/claude-django-unfold-admin.git ~/.claude/skills/unfold-admin
```

That's it. Claude Code will automatically detect and use the skill when you ask about Django admin, unfold, admin actions, admin filters, or admin theming.

### Updating

Pull the latest changes:

```bash
cd ~/.claude/skills/unfold-admin && git pull
```

### Uninstalling

Remove the skill directory:

```bash
rm -rf ~/.claude/skills/unfold-admin
```

## What It Covers

- **Actions and decorators** — `@action` placement options, `@display` decorator for list views, permission handling
- **Filters and search** — Dropdown, radio/checkbox, date/time, numeric, text, and autocomplete filters
- **Inlines and sections** — TabularInline, StackedInline, TableSection, TemplateSection, BaseDataset
- **Settings and configuration** — UNFOLD settings dictionary, branding, colors (OKLch), sidebar navigation, tabs
- **Templates and components** — HTML template patterns, Tailwind CSS classes, Material Symbols icons, dark mode
- **Widgets and styling** — Form widget reference, CSS class constants, Tailwind patterns for form elements

## Usage

Once installed, just ask Claude Code to work on Django admin. The skill triggers automatically. For example:

- "Create a Django admin for my Product model with filters and actions"
- "Add a custom dashboard page to my unfold admin"
- "Style my admin with unfold"
- "Add row-level actions to my OrderAdmin"

## Structure

```
SKILL.md                              # Main skill definition and quick-start guide
examples/
  basic-admin.py                      # Simple ModelAdmin patterns
  advanced-admin.py                   # Full-featured admin with actions, filters, inlines
  settings-example.py                 # Complete UNFOLD settings configuration
  custom-dashboard.html               # Dashboard template with Tailwind styling
references/
  actions-and-decorators.md           # @action and @display decorator reference
  filters-and-search.md              # Filter types and search configuration
  inlines-and-sections.md            # Inlines, TableSection, TemplateSection, BaseDataset
  settings-configuration.md          # UNFOLD settings dictionary reference
  templates-and-components.md        # HTML templates, Tailwind classes, Material Symbols
  widgets-and-styling.md             # Widget reference and CSS class constants
```

## Upstream

- **Package:** [django-unfold](https://github.com/unfoldadmin/django-unfold) (MIT license)
- **Documentation:** [unfoldadmin.com](https://unfoldadmin.com)
- **PyPI:** `pip install django-unfold`

## License

MIT
