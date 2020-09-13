from django.contrib import admin
from .models import Post, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'contents', 'post', 'create_date', 'active')
    list_filter = ('active', 'create_date')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active = True)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','status', 'create_date', 'update_date')
    list_filter = ("create_date",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)

