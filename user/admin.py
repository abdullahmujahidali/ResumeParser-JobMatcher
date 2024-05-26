# Django
# Backend Apps

# Django
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# 3rd Party Libraries
from user.models import User


class AccountCreationForm(forms.ModelForm):

    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "first_name")

    def save(self, commit=True):
        """Save the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AccountChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            'using <a href="../password/">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = ("password",)

    def clean_password(self):
        return self.initial["password"]


class BaseAccountAdmin(BaseUserAdmin):
    """This custom user model is to modify the detail view of a user."""

    form = AccountChangeForm
    add_form = AccountCreationForm
    readonly_fields = ["id", "created_at", "modified_at", "is_owner"]
    ordering = ["id"]
    list_display = [
        "id",
        "email",
        "first_name",
        "is_active",
        "is_owner"
    ]
    fieldsets = (
        (
            "Credentials",
            {
                "fields": (
                    "id",
                    "email",
                    "first_name",
                    "password",
                )
            },
        ),
        (
            "Access control",
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        ("Important times", {"fields": ("created_at", "modified_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "password",
                    "is_active",
                    "is_owner",
                ),
            },
        ),
    )
    filter_horizontal = ()
    list_filter = ()


class UserAdmin(admin.ModelAdmin):
    """This inline model admin displays all the relations of a user with
    tenant inside User model."""

    list_display = [
        "id",
        "user",
    ]
    list_select_related = ("user",)
    readonly_fields = ["id"]


admin.site.register(User, BaseAccountAdmin)
