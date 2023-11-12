from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    objects = models.Manager()

    def __str__(self):
        return f'{self.name}: {self.description}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class BlogPost(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    slug = models.CharField(max_length=300, verbose_name='Slug', **NULLABLE)
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog_previews/', verbose_name='Превью', **NULLABLE)
    created_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, verbose_name='Категория')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='владелец')

    def __str__(self):
        return f'{self.title}: {self.content}'

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'
        ordering = ['-created_date']
