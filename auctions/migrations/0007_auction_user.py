# Generated by Django 2.1.5 on 2020-09-26 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200925_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='user',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
