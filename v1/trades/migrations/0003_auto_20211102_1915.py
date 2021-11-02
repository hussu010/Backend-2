# Generated by Django 3.1.7 on 2021-11-02 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0002_auto_20211102_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='initiator_confirmed',
        ),
        migrations.RemoveField(
            model_name='order',
            name='owner_confirmed',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='fee',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
