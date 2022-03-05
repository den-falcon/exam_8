from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'otzovikapp_category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    category = models.ForeignKey('otzovikapp.Category', default=1, related_name='products', on_delete=models.CASCADE,
                                 verbose_name='Категория')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'otzovikapp_product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), related_name='reviews', on_delete=models.CASCADE,
                               verbose_name='Автор')
    product = models.ForeignKey('otzovikapp.Product', related_name='reviews', on_delete=models.CASCADE,
                                verbose_name='Товар')
    text = models.TextField(max_length=2000, verbose_name='Отзыв')
    rating = models.PositiveIntegerField(verbose_name='Оценка')
    is_moderated = models.BooleanField(verbose_name='Статус модерации', default=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    def __str__(self):
        return f'{self.author} | {self.product}'

    class Meta:
        db_table = 'otzovikapp_review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
