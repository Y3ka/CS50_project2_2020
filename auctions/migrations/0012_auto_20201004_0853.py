# Generated by Django 3.1.1 on 2020-10-04 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='auctions',
            field=models.ManyToManyField(to='auctions.Auction'),
        ),
    ]
