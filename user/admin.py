# Django
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# 3rd Party Libraries
from user.models import User, Qualification, Experience, Project, Skill, Social


class AccountCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "resume")

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
        fields = ("password", "resume")

    def clean_password(self):
        return self.initial["password"]


class QualificationInline(admin.TabularInline):
    model = Qualification
    extra = 1


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class SocialInline(admin.TabularInline):
    model = Social
    extra = 1


class BaseAccountAdmin(BaseUserAdmin):
    """This custom user model is to modify the detail view of a user."""

    form = AccountChangeForm
    add_form = AccountCreationForm
    readonly_fields = ["id", "created_at", "modified_at"]
    ordering = ["id"]
    list_display = [
        "id",
        "email",
        "first_name",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    fieldsets = (
        (
            "Credentials",
            {
                "fields": (
                    "id",
                    "email",
                    "first_name",
                    "last_name",
                    "password",
                )
            },
        ),
        (
            "Personal Info",
            {
                "fields": (
                    "phone_number",
                    "location",
                    "resume",
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
                    "last_name",
                    "password",
                    "is_active",
                    "resume",
                ),
            },
        ),
    )
    filter_horizontal = ()
    list_filter = ()
    inlines = [QualificationInline, ExperienceInline,
               ProjectInline, SkillInline, SocialInline]


admin.site.register(User, BaseAccountAdmin)
