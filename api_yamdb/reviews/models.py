from django.db import models
from users.models import User


class Title(models.Model):
    ...


class Reviews(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Автор'
    )
    score = models.IntegerField(verbose_name='Оценка')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )


class Comments(models.Model):
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments', verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
