# Generated by Django 3.2.14 on 2022-09-10 12:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20220910_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='valid_upto',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 16, 33, 38, 605858)),
        ),
    ]
