"""
Third-Party App Admin Compatibility for Django Unfold

Many third-party Django apps register their own ModelAdmin classes that inherit
from django.contrib.admin.ModelAdmin instead of unfold.admin.ModelAdmin. This
causes them to render with Django's unstyled admin, breaking the look of an
Unfold-themed project.

The fix is always the same pattern:
1. Unregister the default admin class
2. Re-register with a class that inherits from BOTH the original admin AND
   unfold.admin.ModelAdmin (Unfold's ModelAdmin first in MRO)

This file covers the most common offenders:
- django-celery-beat (periodic task scheduling)
- django-celery-results (task result storage)
- django-simple-history (model history tracking)
- django-modeltranslation (model field translations)
- django-hijack (user impersonation)
- djangoql (advanced search)

For integrations that work fully automatically (no admin changes needed):
- django-money: Unfold auto-detects MoneyField and applies UnfoldAdminMoneyWidget
- django-json-widget: Unfold auto-styles the widget with dark mode support

For integrations that need INSTALLED_APPS ordering only:
- django-guardian: Add "unfold.contrib.guardian" near the top of INSTALLED_APPS
- django-hijack: Add "unfold.contrib.hijack" (after unfold, before hijack)
- django-constance: Add "unfold.contrib.constance" before "constance"
- django-location-field: Add "unfold.contrib.location_field" before "location_field"

NOTE on djangoql: Unfold *styles* it automatically, but the search feature is
djangoql's own — you still add "djangoql" to INSTALLED_APPS and inherit
DjangoQLSearchMixin on your admin (see bottom of this file). There is no
unfold.contrib.djangoql app.

Full per-package reference: references/integrations.md
Source: https://unfoldadmin.com/docs/integrations/
"""

from django.contrib import admin

from unfold.admin import ModelAdmin


# =============================================================================
# django-celery-beat
# =============================================================================
# Source: https://unfoldadmin.com/docs/integrations/django-celery-beat/
#
# Package: django-celery-beat
# Models: PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule,
#         ClockedSchedule
#
# These models are auto-registered by celery beat's admin module. You must
# unregister them and re-register with Unfold's ModelAdmin.
#
# IMPORTANT: The PeriodicTask admin needs custom widget/form overrides to
# style the task selector fields properly. Without these, the task and
# registered task dropdowns render with Django's unstyled widgets.

from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget

from django_celery_beat.admin import (
    ClockedScheduleAdmin as BaseClockedScheduleAdmin,
    CrontabScheduleAdmin as BaseCrontabScheduleAdmin,
    PeriodicTaskAdmin as BasePeriodicTaskAdmin,
    PeriodicTaskForm,
    TaskSelectWidget,
)
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    """Combines Unfold styling with celery-beat's task selector functionality."""

    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    """Override the PeriodicTask form to use Unfold-styled widgets.

    The task field (free text) gets UnfoldAdminTextInputWidget.
    The regtask field (registered task dropdown) gets UnfoldTaskSelectWidget.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    """Unfold-styled periodic task admin.

    BasePeriodicTaskAdmin provides the fieldsets, list_display, list_filter,
    search_fields, and the toggle-enabled action. We override the form to use
    Unfold-styled widgets for the task selector fields.
    """

    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    """Unfold-styled interval schedule admin.

    The upstream admin is plain ModelAdmin so we just replace it entirely.
    """

    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    """Unfold-styled crontab schedule admin."""

    pass


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    """Unfold-styled solar schedule admin."""

    pass


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    """Unfold-styled clocked schedule admin."""

    pass


# =============================================================================
# django-celery-results
# =============================================================================
# No official Unfold integration page, but the same pattern applies.
# Package: django-celery-results
# Models: TaskResult, GroupResult
#
# These are auto-registered by django_celery_results.admin.

from django_celery_results.admin import GroupResultAdmin as BaseGroupResultAdmin
from django_celery_results.admin import TaskResultAdmin as BaseTaskResultAdmin
from django_celery_results.models import GroupResult, TaskResult

admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)


@admin.register(TaskResult)
class TaskResultAdmin(BaseTaskResultAdmin, ModelAdmin):
    """Unfold-styled task result admin.

    BaseTaskResultAdmin provides list_display, list_filter, readonly_fields,
    and search_fields. We just add Unfold styling.
    """

    pass


@admin.register(GroupResult)
class GroupResultAdmin(BaseGroupResultAdmin, ModelAdmin):
    """Unfold-styled group result admin.

    BaseGroupResultAdmin provides the full admin configuration for
    group results. We just add Unfold styling.
    """

    pass


# =============================================================================
# django-simple-history
# =============================================================================
# Source: https://unfoldadmin.com/docs/integrations/django-simple-history/
#
# INSTALLED_APPS ordering matters:
#   "unfold",
#   "unfold.contrib.simple_history",   # <-- before simple_history
#   "simple_history",
#
# Then use multiple inheritance in your admin classes:

# from simple_history.admin import SimpleHistoryAdmin
#
# @admin.register(MyModel)
# class MyModelAdmin(SimpleHistoryAdmin, ModelAdmin):
#     pass


# =============================================================================
# django-modeltranslation
# =============================================================================
# Source: https://unfoldadmin.com/docs/integrations/django-modeltranslation/
#
# Use multiple inheritance with TabbedTranslationAdmin:

# from modeltranslation.admin import TabbedTranslationAdmin
#
# @admin.register(MyModel)
# class MyModelAdmin(ModelAdmin, TabbedTranslationAdmin):
#     pass
#
# Optional: add language flags in settings:
# UNFOLD = {
#     "EXTENSIONS": {
#         "modeltranslation": {
#             "flags": {
#                 "en": "🇬🇧",
#                 "fr": "🇫🇷",
#             },
#         },
#     },
# }


# =============================================================================
# django-hijack
# =============================================================================
# Source: https://unfoldadmin.com/docs/integrations/django-hijack/
#
# Styling only — no admin mixin or settings required. Just add the contrib app:
#   INSTALLED_APPS = [
#       "unfold",
#       "unfold.contrib.hijack",   # <-- after unfold, before hijack
#       "hijack",
#       "hijack.contrib.admin",
#   ]
#
# Unfold then styles the impersonation banner and the hijack buttons on the
# user changelist. (The banner may render unstyled once you leave the admin.)


# =============================================================================
# djangoql
# =============================================================================
# Source: https://unfoldadmin.com/docs/integrations/djangoql/
#
# Unfold styles djangoql automatically, but you still wire up djangoql itself:
#   INSTALLED_APPS = ["unfold", "djangoql", ...]
#
# Then inherit djangoql's mixin BEFORE Unfold's ModelAdmin:

# from djangoql.admin import DjangoQLSearchMixin
#
# @admin.register(MyModel)
# class MyModelAdmin(DjangoQLSearchMixin, ModelAdmin):
#     search_fields = ["name"]
