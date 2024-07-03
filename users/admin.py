from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Profile


# Register your models here.
# class CustomUserAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         ("Thông tin thêm", {"fields": ("date_of_birth", "display_name")}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         ("Thông tin thêm", {"fields": ("date_of_birth", "display_name")}),
#     )


# admin.site.register(User, CustomUserAdmin)

admin.site.register(User)
admin.site.register(Profile)
