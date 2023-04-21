from django.contrib import admin
from .models import Author, Category, Post, Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating',)
    list_filter = ('rating',)
    search_fields = ('user__username', 'user__is_staff')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
