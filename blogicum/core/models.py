from django.db import models

from django.utils import timezone


class BasePublishedModel(models.Model):
    '''Абстрактная модель. Добавляет поля is_published и created_at'''

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class PostManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
            pub_date__lt=timezone.now(),
            category__is_published=True
        ).annotate(
            comment_count=models.Count('comments')
        ).order_by('-pub_date')
