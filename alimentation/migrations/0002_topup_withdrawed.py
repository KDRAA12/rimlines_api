# Generated by Django 3.1.7 on 2021-03-11 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alimentation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topup',
            name='withdrawed',
            field=models.BooleanField(default=False),
        ),
    ]
