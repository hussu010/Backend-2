# Generated by Django 3.1.6 on 2021-03-09 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210307_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='memo',
            field=models.CharField(default='tnbcrow-<function uuid4 at 0x03A8F930>', editable=False, max_length=44, unique=True),
        ),
    ]
