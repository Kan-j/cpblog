# Generated by Django 3.2 on 2021-06-13 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_author_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.ImageField(blank=True, default='testing.jpg', upload_to='thumbnail', verbose_name='Picture'),
        ),
    ]
