from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at", "body_preview")
    list_filter = ("created_at",)
    search_fields = ("body", "author__username", "post__title")

    @admin.display(description="Comentario")
    def body_preview(self, obj):
        return obj.body[:60] + "…" if len(obj.body) > 60 else obj.body
