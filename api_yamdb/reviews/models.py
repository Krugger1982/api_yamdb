from django.db import models

class Reviews(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    # #author = models.ForeignKey(
    #     1,
    #     on_delete=models.CASCADE,
    #     related_name='reviews', verbose_name='Автор'
    # )
    score = models.IntegerField(verbose_name='Оценка')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

class Comments(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    # author = models.ForeignKey(
    #     1,
    #     on_delete=models.CASCADE,
    #     related_name='comments', verbose_name='Автор'
    # )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )