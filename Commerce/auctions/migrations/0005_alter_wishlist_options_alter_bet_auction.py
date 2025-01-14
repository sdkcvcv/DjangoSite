# Generated by Django 5.0.2 on 2024-03-09 14:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_wishlist_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wishlist',
            options={'verbose_name': 'Wishlist'},
        ),
        migrations.AlterField(
            model_name='bet',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bet_auction', to='auctions.auction'),
        ),
    ]
