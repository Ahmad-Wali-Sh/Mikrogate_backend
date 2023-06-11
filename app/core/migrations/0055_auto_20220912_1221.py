# Generated by Django 3.2.14 on 2022-09-12 07:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20220912_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='valid_upto',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 12, 12, 21, 12, 719396)),
        ),
        migrations.AlterField(
            model_name='linkdetails',
            name='bill_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='linkdetails',
            name='cable',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='linkdetails',
            name='connector',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='linkdetails',
            name='payment',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
