# Generated by Django 5.0.6 on 2024-06-29 10:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_forum"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="thread",
            name="category",
        ),
        migrations.AddField(
            model_name="thread",
            name="forum",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="threads",
                to="main.forum",
            ),
            preserve_default=False,
        ),
    ]
