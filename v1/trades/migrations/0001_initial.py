# Generated by Django 3.1.7 on 2021-09-10 16:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveTrade',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('rate', models.PositiveIntegerField()),
                ('status', models.IntegerField(choices=[(0, 'Open'), (1, 'Completed'), (2, 'Admin Completed'), (3, 'Owner Cancelled'), (4, 'Initiator Cancelled'), (5, 'Admin Cancelled')], default=0)),
                ('payment_windows', models.PositiveIntegerField()),
                ('terms_of_trade', models.TextField()),
                ('initiator_confirmed', models.BooleanField(default=False)),
                ('owner_confirmed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompletedTrade',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('rate', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TradePost',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('owner_role', models.IntegerField(choices=[(0, 'Buyer'), (1, 'Seller')])),
                ('rate', models.PositiveIntegerField()),
                ('amount', models.PositiveIntegerField()),
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
            name='TradeRequest',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Accepted'), (2, 'Rejected'), (3, 'Cancelled'), (4, 'Expired')], default=0)),
                ('message', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('rate', models.PositiveIntegerField()),
                ('payment_windows', models.PositiveIntegerField()),
                ('terms_of_trade', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expires_at', models.DateTimeField()),
            ],
        ),
    ]
