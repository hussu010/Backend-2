# Generated by Django 3.1.6 on 2021-03-10 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0008_country'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'Countries'},
        ),
        migrations.AddField(
            model_name='country',
            name='phone_code',
            field=models.CharField(default='977', max_length=6),
            preserve_default=False,
        ),
    ]
