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
  user-admin.py                       # User & Group admin (default, AbstractUser, AbstractBaseUser)
  basic-admin.py                      # Simple ModelAdmin patterns
  third-party-admin.py                # Fixing celery-beat, celery-results, hijack, djangoql, etc.
  advanced-admin.py                   # Full-featured admin (actions incl. dialogs, filters, inlines, conditional fields)
  settings-example.py                 # Complete UNFOLD settings configuration
  custom-dashboard.html               # Dashboard using the {% component %} library + Tailwind
references/
  actions-and-decorators.md           # @action (incl. dialogs) and @display decorator reference
  filters-and-search.md              # Filter types, facet/horizontal filters, search
  inlines-and-sections.md            # Inlines (nested/paginated), sections, datasets, conditional fields, sortable
  settings-configuration.md          # UNFOLD settings dict, sidebar, command palette, dashboard
  templates-and-components.md        # HTML templates, Tailwind 4, Material Symbols, dark mode
  components.md                      # Unfold's {% component %} library (cards, charts, tables, buttons, etc.)
  widgets-and-styling.md             # Widget reference and CSS class constants
  integrations.md                    # Third-party packages (celery, hijack, djangoql, import-export, etc.)
```

Targets **django-unfold 0.97.x** (Django ≥ 5.2, Python ≥ 3.12).

## Updating

When django-unfold releases new features or changes APIs, update the corresponding reference file and examples. The SKILL.md quick-start section should stay in sync with the current API surface. Ground new content in the upstream docs ([unfoldadmin.com/docs](https://unfoldadmin.com/docs/)) and source ([github.com/unfoldadmin/django-unfold](https://github.com/unfoldadmin/django-unfold)) rather than memory — Unfold's API moves quickly. Bump the "Version & Compatibility" block in SKILL.md when the supported Django/Python range changes.

See [`MAINTAINING.md`](MAINTAINING.md) for the full step-by-step refresh procedure (version delta → per-cluster grounded research → apply → retrieval-test verification).
