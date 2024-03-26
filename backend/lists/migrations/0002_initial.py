# Generated by Django 4.1.13 on 2024-03-26 22:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("films", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("lists", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="list",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="list",
            name="compilation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="lists.compilation"
            ),
        ),
        migrations.AddField(
            model_name="list",
            name="films",
            field=models.ManyToManyField(through="lists.ListFilm", to="films.film"),
        ),
        migrations.AddField(
            model_name="compilation",
            name="owners",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name="listfilm",
            unique_together={("film", "list")},
        ),
        migrations.AlterUniqueTogether(
            name="list",
            unique_together={("compilation", "author")},
        ),
    ]
