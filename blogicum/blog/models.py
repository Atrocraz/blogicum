from django.db import models
from core.models import BaseModel, PostManager
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(BaseModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField('Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(BaseModel):
    objects = models.Manager()
    published = PostManager()

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации',
    )

    location = models.ForeignKey(
        Location,
        related_name='posts',
        verbose_name='Местоположение',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )

    image = models.ImageField('Фото', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
