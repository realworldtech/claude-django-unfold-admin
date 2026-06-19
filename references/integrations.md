# Third-Party Integrations Reference

How to make popular Django packages render correctly under Unfold. Verified against the official docs and source for django-unfold 0.97.x.

## How Unfold integrates with other packages

There are three mechanisms, and it matters which one a package uses:

1. **Template-override contrib app** — add an `unfold.contrib.*` app to `INSTALLED_APPS` so Unfold's templates win. Used by: `constance`, `guardian`, `hijack`, `import_export`, `location_field`, `simple_history`.
2. **Multiple inheritance** — combine the package's admin class with `unfold.admin.ModelAdmin`. Used by: import-export, simple-history, modeltranslation, guardian, djangoql, celery-beat.
3. **Automatic (CSS only)** — Unfold detects and styles the package's widgets with no setup. Used by: django-money, django-json-widget, and djangoql's *styling*.

### The complete `unfold.contrib.*` module list (0.97.x)

| Module | Kind | Purpose |
|--------|------|---------|
| `unfold.contrib.filters` | Unfold feature | Advanced list filters (range, dropdown, slider, autocomplete) |
| `unfold.contrib.forms` | Unfold feature | Form widgets `ArrayWidget`, `WysiwygWidget` |
| `unfold.contrib.inlines` | Unfold feature | Non-related & enhanced inlines |
| `unfold.contrib.import_export` | Integration | django-import-export styled forms |
| `unfold.contrib.simple_history` | Integration | django-simple-history templates |
| `unfold.contrib.guardian` | Integration | django-guardian object-permission templates |
| `unfold.contrib.hijack` | Integration | django-hijack templates |
| `unfold.contrib.constance` | Integration | django-constance templates + field defs |
| `unfold.contrib.location_field` | Integration | django-location-field widget |

There is **no** `unfold.contrib.djangoql`, `unfold.contrib.crispy`, `unfold.contrib.modeltranslation`, `unfold.contrib.money`, or `unfold.contrib.celery_beat` — those are handled by inheritance, settings, or automatic CSS.

> **MRO is not uniform across integrations.** Some put `ModelAdmin` first, some put the third-party class first. Follow each section exactly rather than normalizing.

---

## django-celery-beat (+ django-celery-results)

The most common case. No contrib app — you unregister the default admins and re-register them combined with `ModelAdmin`, plus override the `PeriodicTask` form widgets (otherwise the task selector renders unstyled). This mirrors the [official guide](https://unfoldadmin.com/docs/integrations/django-celery-beat/).

```python
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget

from django_celery_beat.models import (
    ClockedSchedule, CrontabSchedule, IntervalSchedule, PeriodicTask, SolarSchedule,
)
from django_celery_beat.admin import (
    ClockedScheduleAdmin as BaseClockedScheduleAdmin,
    CrontabScheduleAdmin as BaseCrontabScheduleAdmin,
    PeriodicTaskAdmin as BasePeriodicTaskAdmin,
    PeriodicTaskForm,
    TaskSelectWidget,
)

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass
```

`IntervalSchedule`/`SolarSchedule` have no upstream admin worth keeping, so they inherit `ModelAdmin` only; the others inherit `Base…Admin, ModelAdmin`.

**django-celery-results** has no official Unfold page, but the same unregister/re-register pattern works for its `TaskResult` and `GroupResult` models (inherit `Base…Admin, ModelAdmin`). See `examples/third-party-admin.py`.

---

## django-import-export

```python
# settings.py — unfold.contrib.import_export before import_export
INSTALLED_APPS = ["unfold", "unfold.contrib.import_export", "import_export", "django.contrib.admin", ...]
```

```python
from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin, ImportExportModelAdmin):   # ModelAdmin FIRST
    import_form_class = ImportForm
    export_form_class = ExportForm
    # export_form_class = SelectableFieldsExportForm   # to pick fields on export
```

- MRO: `ModelAdmin` first, `ImportExportModelAdmin` second.
- Unfold provides **no** `ImportExportModelAdmin` of its own — only the styled form classes.
- `ExportActionModelAdmin` is no longer needed in django-import-export 4.x+.

---

## django-simple-history

```python
# settings.py — order matters
INSTALLED_APPS = ["unfold", "unfold.contrib.simple_history", "simple_history", "django.contrib.admin", ...]
```

```python
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin

@admin.register(MyModel)
class MyModelAdmin(SimpleHistoryAdmin, ModelAdmin):   # SimpleHistoryAdmin FIRST
    pass
```

---

## django-modeltranslation

No contrib app. Multiple inheritance with `ModelAdmin` **first**, and configure flags via `UNFOLD["EXTENSIONS"]`.

```python
# settings.py
UNFOLD = {
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {"en": "🇬🇧", "fr": "🇫🇷", "nl": "🇧🇪"},
        },
    },
}
```

```python
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin, TabbedTranslationAdmin):   # ModelAdmin FIRST
    pass
```

---

## django-hijack

Styling only. Add the contrib app; no admin mixin or settings required.

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.hijack",   # after unfold, before hijack
    "hijack",
    "hijack.contrib.admin",
    ...,
]
```

Unfold styles the "impersonating" banner and the hijack buttons on the user changelist. Known limitation: the banner may render unstyled once you leave the admin (admin CSS is no longer loaded).

---

## djangoql

**Styling is automatic; the search feature is not.** Unfold styles djangoql's search input, toggle, and dropdown with no Unfold-specific config, but you still set up djangoql itself: add `"djangoql"` to `INSTALLED_APPS` and inherit its mixin (before `ModelAdmin`).

```python
from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin
from unfold.admin import ModelAdmin

@admin.register(MyModel)
class MyModelAdmin(DjangoQLSearchMixin, ModelAdmin):   # mixin FIRST
    search_fields = ["name"]
```

(djangoql's own embedded help pages are not styled by Unfold.)

---

## django-guardian

Add the contrib app near the **top** of `INSTALLED_APPS` (so it overrides guardian's templates), keep guardian's own backend, then combine `GuardedModelAdmin` with `ModelAdmin`. Unfold adds an "Object permissions" button to the change form.

```python
# settings.py
INSTALLED_APPS = ["unfold", "unfold.contrib.guardian", "guardian", "django.contrib.admin", ...]
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]
```

```python
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from unfold.admin import ModelAdmin

@admin.register(MyModel)
class MyModelAdmin(GuardedModelAdmin, ModelAdmin):
    pass
```

---

## django-constance

Add the contrib app **before** `constance`, then merge Unfold's field definitions into `CONSTANCE_ADDITIONAL_FIELDS`.

```python
# settings.py
INSTALLED_APPS = ["unfold", "unfold.contrib.constance", "constance", ...]

from unfold.contrib.constance.settings import UNFOLD_CONSTANCE_ADDITIONAL_FIELDS

CONSTANCE_ADDITIONAL_FIELDS = {
    **UNFOLD_CONSTANCE_ADDITIONAL_FIELDS,
    "choice_field": [
        "django.forms.fields.ChoiceField",
        {
            "widget": "unfold.widgets.UnfoldAdminSelectWidget",
            "choices": (("light-blue", "Light blue"), ("dark-blue", "Dark blue")),
        },
    ],
}
```

`UNFOLD_CONSTANCE_ADDITIONAL_FIELDS` maps `str`/`int`/`float`/`bool` plus `"file_field"`/`"image_field"` to Unfold-styled widgets.

---

## django-location-field

Add the contrib app **before** `location_field`, then swap the widget on a custom form.

```python
# settings.py
INSTALLED_APPS = ["unfold", "unfold.contrib.location_field", "location_field", ...]
```

```python
from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.location_field.widgets import UnfoldAdminLocationWidget

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["location"].widget = UnfoldAdminLocationWidget()  # base_fields=[...], zoom=7

@admin.register(Place)
class PlaceAdmin(ModelAdmin):
    form = PlaceForm
```

---

## django-crispy-forms

The `unfold_crispy` template pack ships **inside core unfold** — there is no `unfold.contrib.crispy`. You only need `crispy_forms` installed plus the settings.

```python
# settings.py
INSTALLED_APPS = ["unfold", "crispy_forms", ...]
CRISPY_ALLOWED_TEMPLATE_PACKS = ["unfold_crispy"]
CRISPY_TEMPLATE_PACK = "unfold_crispy"
```

```django
{% load crispy_forms_tags %}
{% crispy form "unfold_crispy" %}
```

---

## django-money & django-json-widget (automatic)

Nothing to add to `INSTALLED_APPS`. Unfold detects and styles their widgets automatically. (If you want explicit control, `unfold.widgets.UnfoldAdminMoneyWidget` exists, but it is not required.)

---

## General fix pattern (any package that registers its own admin)

When a package registers admin classes that inherit Django's plain `ModelAdmin`:

1. **Unregister** the default admin.
2. **Re-register** with a class inheriting from BOTH the package's admin AND `unfold.admin.ModelAdmin`.
3. Check whether the package documents a specific MRO; when in doubt, try the third-party base first, then `ModelAdmin`.

```python
from django.contrib import admin
from unfold.admin import ModelAdmin
from some_package.admin import SomeModelAdmin as BaseSomeModelAdmin
from some_package.models import SomeModel

admin.site.unregister(SomeModel)

@admin.register(SomeModel)
class SomeModelAdmin(BaseSomeModelAdmin, ModelAdmin):
    pass
```

## When to apply this

- **During initial Unfold setup:** scan `INSTALLED_APPS`, fix every third-party admin before the user sees broken pages.
- **When adding a new third-party app:** check whether it registers admin classes or ships widgets, and apply the right mechanism.
- **When debugging "some admin pages look unstyled":** this is almost always an un-converted third-party admin.
