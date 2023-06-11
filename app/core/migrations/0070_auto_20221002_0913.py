# Generated by Django 3.2.15 on 2022-10-02 04:43

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_auto_20220928_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contracts',
            name='activation',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 2, 9, 13, 39, 28061)),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 2, 9, 13, 39, 28036)),
        ),
        migrations.AlterField(
            model_name='contracts',
            name='valid',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 2, 9, 13, 39, 28078)),
        ),
        migrations.AlterField(
            model_name='task',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.contracts'),
        ),
        migrations.DeleteModel(
            name='Contract',
        ),
    ]
