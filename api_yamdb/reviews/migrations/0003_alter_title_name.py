# Generated by Django 3.2 on 2023-01-13 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230113_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
    ]
