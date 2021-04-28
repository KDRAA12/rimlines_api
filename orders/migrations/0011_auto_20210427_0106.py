# Generated by Django 3.1.7 on 2021-04-27 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20210427_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(to='orders.Media'),
        ),
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='orders.media'),
        ),
    ]
