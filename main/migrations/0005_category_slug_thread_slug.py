# Generated by Django 5.0.6 on 2024-06-27 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_category_options_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AddField(
            model_name='thread',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
