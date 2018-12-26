from django.contrib import admin

from .models import Tag, TagCount, Post, TagPriority, TextSearch, Profile


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'name', 'languages')
    list_display = ('get_uuid', 'name', 'last_count', 'languages')
    ordering = ('name',)


@admin.register(TagCount)
class TagCountModelAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'tag__name')
    list_display = ('get_uuid', 'tag', 'count')
    ordering = ('tag',)


# class IngestAtFilter(admin.SimpleListFilter):
#     title = 'Injest At'
#     parameter_name = 'ingest_at__isnull'
#
#     def lookups(self, request, model_admin):
#         return (
#             ('False', 'has injested'),
#             ('True', 'has no injested'),
#         )
#
#     def queryset(self, request, queryset):
#         if self.value() == 'False':
#             return queryset.filter(ingest_at__isnull=False)
#         if self.value() == 'True':
#             return queryset.filter(ingest_at__isnull=True)


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    # list_filter = (IngestAtFilter,)
    search_fields = ('uuid', 'shortcode', 'tags')
    list_display = ('get_uuid', 'shortcode', 'ingest_at', 'tags')
    ordering = ('shortcode',)


@admin.register(TagPriority)
class TagPriorityModelAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'tag_name')
    list_display = ('get_uuid', 'tag')
    ordering = ('tag__name',)


class IngestAtFilter(admin.SimpleListFilter):
    title = 'Ingest At'
    parameter_name = 'ingest_at__isnull'

    def lookups(self, request, model_admin):
        return (
            ('False', 'has ingested'),
            ('True', 'has no ingested'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'False':
            return queryset.filter(ingest_at__isnull=False)
        if self.value() == 'True':
            return queryset.filter(ingest_at__isnull=True)


@admin.register(TextSearch)
class TextSearchModelAdmin(admin.ModelAdmin):
    list_filter = (IngestAtFilter,)
    search_fields = ('uuid', 'text')
    list_display = ('get_uuid', 'text', 'result', 'status', 'ingest_at')


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'identifier')
    list_display = ('get_uuid', 'identifier')
