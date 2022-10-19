# Generated by Django 4.0.3 on 2022-09-20 00:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews_rest', '0002_alter_review_post_alter_review_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='post',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]