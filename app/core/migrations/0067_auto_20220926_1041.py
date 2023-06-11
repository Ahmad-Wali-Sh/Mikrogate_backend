# Generated by Django 3.2.15 on 2022-09-26 06:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_auto_20220924_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='changelocation',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='contract',
            name='contract_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 26, 10, 41, 7, 339835)),
        ),
        migrations.AlterField(
            model_name='contract',
            name='valid_upto',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 26, 10, 41, 7, 339835)),
        ),
    ]
