from django.contrib import admin
from .models import Category, Thread, Post


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ThreadAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post)
