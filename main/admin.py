from django.contrib import admin

from .models import Thread, Forum, Comment


# Register your actions here.


@admin.action(description="Pin selected threads")
def pin_threads(modeladmin, request, queryset):
    queryset.update(is_pinned=True)


@admin.action(description="Unpin selected threads")
def unpin_threads(modeladmin, request, queryset):
    queryset.update(is_pinned=False)


# Register your models here.


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_filter = ("created_at",)
    prepopulated_fields = {"slug": ("name",)}
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "forum",
        "is_pinned",
    )
    list_filter = ("created_at",)
    prepopulated_fields = {"slug": ("title",)}
    actions = [pin_threads, unpin_threads]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "content",
        "thread",
    )
    list_filter = ("created_at",)
    show_facets = admin.ShowFacets.ALWAYS
