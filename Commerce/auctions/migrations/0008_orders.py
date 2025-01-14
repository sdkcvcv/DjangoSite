# Generated by Django 5.0.2 on 2024-06-18 07:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auction_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('auction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_auc_title', to='auctions.auction')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='orderer', to=settings.AUTH_USER_MODEL, verbose_name='orderer')),
            ],
            options={
                'verbose_name': 'Orders',
            },
        ),
    ]
