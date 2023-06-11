# Generated by Django 3.2.14 on 2022-08-28 05:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20220828_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='valid_upto',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 28, 10, 20, 32, 693877)),
        ),
        migrations.AlterField(
            model_name='taskmanager',
            name='log_note',
            field=models.TextField(blank=True),
        ),
    ]
