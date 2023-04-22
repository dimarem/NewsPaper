from django.contrib import admin
from .models import Author, Category, Post, Comment
from modeltranslation.admin import TranslationAdmin


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating',)
    list_filter = ('rating',)
    search_fields = ('user__username', 'user__is_staff')


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
