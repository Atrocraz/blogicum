from django.db import models

from datetime import datetime


class BaseModel(models.Model):
    '''Абстрактная модель. Добавляет поля is_published и created_at'''
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True

# https://docs.djangoproject.com/en/4.2/topics/db/managers/#modifying-a-manager-s-initial-queryset

# class PostQuerySet(models.QuerySet):
#     def published(self):
#         return self.filter(
#             is_published=True,
#             pub_date__lt=datetime.now(),
#             category__is_published=True
#         )


class PostManager(models.Manager):
    def get_queryset(self):
        # return PostQuerySet(self.model, using=self._db)
        return super().get_queryset().filter(
            is_published=True,
            pub_date__lt=datetime.now(),
            category__is_published=True
        )

    # def published(self):
    #     return self.get_queryset().published()
