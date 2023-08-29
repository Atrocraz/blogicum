from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.models import BasePublishedModel, PostManager

User = get_user_model()

MAX_TITLE_LEN = 30


class Category(BasePublishedModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField('Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:MAX_TITLE_LEN]


class Location(BasePublishedModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:MAX_TITLE_LEN]


class Post(BasePublishedModel):
    objects = models.Manager()
    published = PostManager()

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )

    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    image = models.ImageField('Фото', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.id})

    def __str__(self):
        return self.title[:MAX_TITLE_LEN]


class Comment(models.Model):
    text = models.TextField('Текст')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return (f'Пост № {self.post.id}, '
                'комментарий пользователя {self.author}, '
                'текст {self.post[:10]}')
