# Generated by Django 3.2.13 on 2022-07-03 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_contract_curren'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='curren',
            field=models.CharField(blank=True, default='AFN', max_length=5),
        ),
    ]