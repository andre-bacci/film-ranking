# Generated by Django 4.1.13 on 2024-04-01 01:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lists", "0003_alter_list_compilation_alter_listfilm_film"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listfilm",
            name="ranking",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
    ]
