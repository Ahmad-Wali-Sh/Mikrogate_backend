# Generated by Django 3.2.14 on 2022-08-23 05:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20220823_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='valid_upto',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 23, 10, 11, 32, 611367)),
        ),
    ]