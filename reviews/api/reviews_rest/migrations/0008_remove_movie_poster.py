# Generated by Django 4.0.3 on 2022-08-23 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews_rest', '0007_remove_movie_actors_remove_movie_director_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='poster',
        ),
    ]
