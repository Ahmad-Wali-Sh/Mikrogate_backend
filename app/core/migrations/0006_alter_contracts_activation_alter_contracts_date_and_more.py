# Generated by Django 4.1.5 on 2023-08-21 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_contracts_activation_alter_contracts_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contracts',
            name='activation',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='valid',
            field=models.DateTimeField(),
        ),
    ]
