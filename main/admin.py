from django.contrib import admin
from .models import Thread, Forum, Comment


# Register your models here.
class ForumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ThreadAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment)
