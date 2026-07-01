"""
Django Unfold User & Group Admin Example

Covers three scenarios:
1. Default Django User model (auth.User)
2. Custom User model extending AbstractUser
3. Custom User model extending AbstractBaseUser

In all cases you must unregister the default admin and re-register with
Unfold's ModelAdmin and styled forms.
"""

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm


# =============================================================================
# Scenario 1: Default Django User (auth.User)
# =============================================================================
# Use this when your project uses the built-in django.contrib.auth.models.User.

from django.contrib.auth.models import User  # noqa: E402

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """
    Unfold-styled admin for the default Django User model.

    Key points:
    - Inherit from BOTH BaseUserAdmin and ModelAdmin (order matters).
    - Override form, add_form, and change_password_form with Unfold versions.
    - BaseUserAdmin already defines fieldsets, add_fieldsets, list_display,
      list_filter, and search_fields. Override only what you need to customise.
    """

    # Required: Unfold-styled forms
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    # Optional: customise list display with Unfold decorators
    list_display = [
        "username",
        "email",
        "display_full_name",
        "display_staff",
        "display_active",
    ]
    list_filter = ["is_staff", "is_superuser", "is_active", "groups"]

    @display(description=_("Name"), header=True)
    def display_full_name(self, obj):
        return obj.get_full_name() or obj.username, obj.email

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, obj):
        return obj.is_staff

    @display(
        description=_("Active"),
        label={
            "Active": "success",
            "Inactive": "danger",
        },
    )
    def display_active(self, obj):
        return _("Active") if obj.is_active else _("Inactive")


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """
    Unfold-styled admin for the default Django Group model.

    Typically no customisation is needed beyond inheriting from both
    BaseGroupAdmin and ModelAdmin.
    """

    pass


# =============================================================================
# Scenario 2: Custom User extending AbstractUser
# =============================================================================
# Use this when your project defines a custom user model that extends
# AbstractUser (i.e. it keeps username, email, first_name, last_name, etc.
# but adds extra fields).
#
# In your models.py:
#
#   from django.contrib.auth.models import AbstractUser
#
#   class CustomUser(AbstractUser):
#       phone = models.CharField(max_length=20, blank=True)
#       department = models.ForeignKey("Department", null=True, blank=True, ...)
#
# In settings.py:
#   AUTH_USER_MODEL = "accounts.CustomUser"

"""
from accounts.models import CustomUser

# If your custom user is registered by default (e.g. via another app), unregister first:
# admin.site.unregister(CustomUser)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    # Extend the default fieldsets to include your custom fields
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {
            "fields": ("first_name", "last_name", "email", "phone", "department"),
        }),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
            "classes": ["tab"],
        }),
        (_("Important dates"), {
            "fields": ("last_login", "date_joined"),
            "classes": ["tab"],
        }),
    )

    # add_fieldsets controls the form shown when creating a NEW user.
    # This is a Django UserAdmin convention, not a standard ModelAdmin attribute.
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )

    list_display = [
        "username",
        "email",
        "display_full_name",
        "department",
        "display_staff",
        "display_active",
    ]
    list_filter = ["is_staff", "is_superuser", "is_active", "groups", "department"]
    search_fields = ["username", "first_name", "last_name", "email"]

    @display(description=_("Name"), header=True)
    def display_full_name(self, obj):
        return obj.get_full_name() or obj.username, obj.email

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, obj):
        return obj.is_staff

    @display(
        description=_("Active"),
        label={
            "Active": "success",
            "Inactive": "danger",
        },
    )
    def display_active(self, obj):
        return _("Active") if obj.is_active else _("Inactive")
"""


# =============================================================================
# Scenario 3: Custom User extending AbstractBaseUser
# =============================================================================
# Use this when your user model does NOT use username at all (e.g. email-only
# auth). Since AbstractBaseUser has no fieldsets defined, you must provide
# them entirely.
#
# In your models.py:
#
#   from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#
#   class EmailUser(AbstractBaseUser, PermissionsMixin):
#       email = models.EmailField(unique=True)
#       full_name = models.CharField(max_length=255)
#       is_staff = models.BooleanField(default=False)
#       is_active = models.BooleanField(default=True)
#       date_joined = models.DateTimeField(auto_now_add=True)
#
#       USERNAME_FIELD = "email"
#       REQUIRED_FIELDS = ["full_name"]
#
# In settings.py:
#   AUTH_USER_MODEL = "accounts.EmailUser"

"""
from accounts.models import EmailUser


@admin.register(EmailUser)
class EmailUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    # IMPORTANT: When using AbstractBaseUser, you must define fieldsets and
    # add_fieldsets yourself since BaseUserAdmin defaults assume username exists.
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {
            "fields": ("full_name",),
        }),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
            "classes": ["tab"],
        }),
        (_("Important dates"), {
            "fields": ("last_login", "date_joined"),
            "classes": ["tab"],
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2"),
        }),
    )

    # Override these BaseUserAdmin defaults since there is no username field
    list_display = [
        "email",
        "display_name",
        "display_staff",
        "display_active",
        "date_joined",
    ]
    list_filter = ["is_staff", "is_superuser", "is_active", "groups"]
    search_fields = ["email", "full_name"]
    ordering = ["email"]

    @display(description=_("Name"), header=True)
    def display_name(self, obj):
        return obj.full_name, obj.email

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, obj):
        return obj.is_staff

    @display(
        description=_("Active"),
        label={
            "Active": "success",
            "Inactive": "danger",
        },
    )
    def display_active(self, obj):
        return _("Active") if obj.is_active else _("Inactive")
"""
