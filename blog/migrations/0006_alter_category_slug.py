# Generated by Django 3.2 on 2021-06-14 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='Slug'),
        ),
    ]
