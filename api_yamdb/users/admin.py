from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
    )
    list_display_links = ("pk", "username", "email")
    search_fields = ("username", "email", "first_name", "last_name")
    list_editable = ("role", "first_name", "last_name")
    list_filter = ("role",)

    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
