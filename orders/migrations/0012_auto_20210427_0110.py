# Generated by Django 3.1.7 on 2021-04-27 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20210427_0106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=models.ImageField(upload_to=''),
        ),
    ]
