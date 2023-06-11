# Generated by Django 3.2.14 on 2022-09-12 18:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_auto_20220912_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='valid_upto',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 12, 22, 57, 17, 636338)),
        ),
        migrations.AlterField(
            model_name='linkdetails',
            name='installation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 12, 22, 57, 17, 645355)),
        ),
        migrations.AlterField(
            model_name='onlinesupport',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]