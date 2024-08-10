# Generated by Django 5.0.2 on 2024-06-18 08:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_orders_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_auc_title', to='auctions.auction'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderer', to=settings.AUTH_USER_MODEL, verbose_name='orderer'),
        ),
    ]