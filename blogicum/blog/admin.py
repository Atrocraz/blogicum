from django.contrib import admin
# from django.utils.safestring import mark_safe
from django.utils.html import format_html

from blog.models import Category, Location, Post, Comment

admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        # 'short_image',
        'image_tag',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'pub_date',
        'author',
        'is_published'
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="60" />'.format(obj.image.url)
            )

    image_tag.short_description = 'Изображение'
    # Вариант выше работает отлично
    # Этот код оставил тут закомментированным, чтобы разобраться позднее
    # @admin.display(description='Изображение')
    # def short_image(self, obj):
    #     if obj.image:
    #         return mark_safe(
    #             f'<img scr="{obj.image.url}" width="80" height="60">'
    #         )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published'
    )
    list_editable = (
        'description',
        'slug',
        'is_published'
    )
    search_fields = ('title',)
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published'
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',)
    list_display_links = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author'
    )
    search_fields = ('author', 'post_id',)
    list_display_links = ('author',)
