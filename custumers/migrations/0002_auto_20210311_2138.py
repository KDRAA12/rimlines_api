# Generated by Django 3.1.7 on 2021-03-11 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custumers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.CharField(blank=True, choices=[('deposit_agent', 'deposit_agent'), ('collector', 'collector')], max_length=300, null=True),
        ),
    ]
