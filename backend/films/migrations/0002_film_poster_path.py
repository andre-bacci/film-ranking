# Generated by Django 4.1.13 on 2024-04-01 12:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("films", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="film",
            name="poster_path",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
