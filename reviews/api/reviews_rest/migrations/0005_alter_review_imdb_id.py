# Generated by Django 4.0.3 on 2022-08-23 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews_rest', '0004_alter_review_imdb_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='imdb_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='reviews_rest.movie'),
        ),
    ]