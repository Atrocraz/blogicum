from django.contrib import admin
from django.utils.safestring import mark_safe

from blog.models import Category, Location, Post, Comment

admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'short_image',
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

    # По какой-то причине не работает, не смог разобраться
    # Url передаёт верно, но картинки всё равно нет
    @admin.display(description='Изображение')
    def short_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img scr="{obj.image.url}" width="80" height="60">'
            )


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
    )
    search_fields = ('author_id', 'post_id',)
    list_display_links = ('author_id',)
