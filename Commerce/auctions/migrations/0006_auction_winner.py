# Generated by Django 5.0.2 on 2024-03-09 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_wishlist_options_alter_bet_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='winner',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
