# Generated by Django 3.2.14 on 2022-08-27 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20220823_1012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='Contract_date',
            new_name='contract_date',
        ),
        migrations.AlterField(
            model_name='contract',
            name='activation_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='valid_upto',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 27, 16, 54, 57, 30079)),
        ),
    ]