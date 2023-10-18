from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets += (("Array fields", {"fields": ("user_type", "user_status")}),)
        return fieldsets

    list_display = (
        "username",
        "first_name",
        "last_name",
        "user_type_display",
        "user_status_display",
    )

    def user_type_display(self, obj):
        return obj.user_type

    def user_status_display(self, obj):
        return obj.user_status
