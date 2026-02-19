# Unfold Admin Skill

A Claude Code skill that provides comprehensive reference documentation and examples for building modern Django admin interfaces with [django-unfold](https://github.com/unfoldadmin/django-unfold).

## What This Is

This is a **Claude Code skill** — a structured knowledge pack that Claude Code loads when a user asks to build or modify Django admin pages using django-unfold. It contains no runtime code; it's entirely reference documentation and examples that guide Claude Code to produce correct, well-styled admin interfaces.

## How It's Used

This skill is installed into `~/.claude/skills/unfold-admin/` and is automatically invoked when a user mentions Django admin, unfold, admin actions, admin filters, or admin theming. Claude Code reads the relevant reference files before writing any code, ensuring it uses the correct Tailwind classes, component patterns, and API conventions rather than guessing.

## Upstream Project

- **Package:** [django-unfold](https://github.com/unfoldadmin/django-unfold) (MIT license)
- **Documentation:** [unfoldadmin.com](https://unfoldadmin.com)
- **PyPI:** `pip install django-unfold`

This skill is not affiliated with the django-unfold project. It is an independently maintained reference guide built from the public documentation and source code.

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

## Updating

When django-unfold releases new features or changes APIs, update the corresponding reference file and examples. The SKILL.md quick-start section should stay in sync with the current API surface.
