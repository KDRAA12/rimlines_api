# Generated by Django 3.1.7 on 2021-04-27 03:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20210427_0110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='is_used',
        ),
        migrations.AddField(
            model_name='good',
            name='adding_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='good',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='good',
            name='status',
            field=models.CharField(choices=[('SENT', 'sent'), ('OPENED', 'opened'), ('UNUSED', 'unused')], default='UNUSED', max_length=300),
        ),
    ]
