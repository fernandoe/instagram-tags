from django.contrib import admin

from .models import Tag, TagCount, Post


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'name')
    list_display = ('get_uuid', 'name')
    ordering = ('name',)


@admin.register(TagCount)
class TagCountModelAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'tag__name')
    list_display = ('get_uuid', 'tag', 'count')
    ordering = ('tag',)


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'shortcode', 'tags')
    list_display = ('get_uuid', 'shortcode', 'tags')
    ordering = ('shortcode',)
