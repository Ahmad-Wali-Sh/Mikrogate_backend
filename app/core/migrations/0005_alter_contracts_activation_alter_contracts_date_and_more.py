# Generated by Django 4.1.5 on 2023-08-21 11:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_contracts_activation_alter_contracts_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contracts',
            name='activation',
            field=models.DateField(default=datetime.datetime(2023, 8, 21, 15, 56, 45, 663832)),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 8, 21, 15, 56, 45, 663805)),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='valid',
            field=models.DateField(default=datetime.datetime(2024, 8, 21, 15, 56, 45, 663899)),
        ),
    ]