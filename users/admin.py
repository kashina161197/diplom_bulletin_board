from django.contrib import admin

from users.models import CustomsUser


@admin.register(CustomsUser)
class CustomUserAdmin(admin.ModelAdmin):
    """ "Отображение информации в панеле админа"""

    list_display = ("id", "email", "role", "is_staff", "is_active", "is_superuser")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email",)
