# Generated by Django 5.0.2 on 2024-05-30 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auction_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
