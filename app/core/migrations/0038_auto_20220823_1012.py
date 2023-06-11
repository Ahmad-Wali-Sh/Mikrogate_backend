# Generated by Django 3.2.14 on 2022-08-23 05:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_alter_contract_valid_upto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='activation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='valid_upto',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 23, 10, 12, 48, 950582)),
        ),
    ]
