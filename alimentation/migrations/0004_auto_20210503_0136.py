# Generated by Django 3.1.7 on 2021-05-03 01:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alimentation', '0003_versement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='versement',
            name='versed_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]