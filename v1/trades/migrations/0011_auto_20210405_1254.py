# Generated by Django 3.1.7 on 2021-04-05 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0010_tradepost_payment_windows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradepost',
            name='payment_windows',
            field=models.IntegerField(),
        ),
    ]
