# Generated by Django 3.2 on 2021-06-12 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, default='testing.jpg', upload_to='thumbnail', verbose_name='Thumbnail'),
        ),
    ]