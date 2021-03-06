# Generated by Django 3.1.7 on 2021-11-04 06:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('BUYER', 'Buyer'), ('SELLER', 'Seller')], max_length=255)),
                ('rate', models.PositiveIntegerField()),
                ('amount', models.PositiveIntegerField()),
                ('fee', models.BigIntegerField()),
                ('payment_windows', models.PositiveIntegerField()),
                ('terms_of_trade', models.TextField()),
                ('min_reputation', models.IntegerField()),
                ('broadcast_trade', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('rate', models.PositiveIntegerField()),
                ('fee', models.IntegerField()),
                ('payment_windows', models.PositiveIntegerField()),
                ('terms_of_trade', models.TextField()),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('COMPLETED', 'Completed'), ('ADMIN_COMPLETED', 'Admin Completed'), ('TAKER_CANCELLED', 'Taker Cancelled'), ('MAKER_CANCELLED', 'Maker Cancelled'), ('ADMIN_CANCELLED', 'Admin Cancelled')], default='OPEN', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trades.advertisement')),
            ],
        ),
    ]
