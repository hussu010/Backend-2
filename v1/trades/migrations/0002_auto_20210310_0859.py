# Generated by Django 3.1.6 on 2021-03-10 03:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trades', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('constants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='traderequest',
            name='initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='traderequest',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trades.tradepost'),
        ),
        migrations.AddField(
            model_name='tradepost',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tradepost',
            name='transaction_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constants.transactiontype'),
        ),
        migrations.AddField(
            model_name='completedtrade',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='completedtrade',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activetrade',
            name='initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activetrade',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trades.tradepost'),
        ),
    ]
