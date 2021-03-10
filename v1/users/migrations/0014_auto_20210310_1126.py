# Generated by Django 3.1.6 on 2021-03-10 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20210310_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='user',
            name='memo',
            field=models.CharField(default='tnbcrow-<function uuid4 at 0x03BEF978>', editable=False, max_length=44, unique=True),
        ),
    ]