# Generated by Django 3.1.7 on 2021-04-27 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_product_require_manual_activation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='being_delivered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ordered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='received',
        ),
        migrations.RemoveField(
            model_name='order',
            name='refund_granted',
        ),
        migrations.RemoveField(
            model_name='order',
            name='refund_requested',
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='good',
            name='images',
            field=models.ManyToManyField(to='orders.Media'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[(-2, 'REQUEST REFUND'), (-1, 'REFUND GRANTED'), (0, 'PRODUCT NEED RESTOCK'), (1, 'AGENT NEEDED FOR ACTIVATION'), (2, 'ORDER  COMPLETED')], max_length=300, null=True),
        ),
    ]