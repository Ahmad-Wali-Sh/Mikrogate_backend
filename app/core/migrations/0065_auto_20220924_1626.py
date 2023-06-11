# Generated by Django 3.2.15 on 2022-09-24 11:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0064_auto_20220924_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changelocation',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.task'),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.task'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='contract_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 24, 16, 26, 29, 88434)),
        ),
        migrations.AlterField(
            model_name='contract',
            name='valid_upto',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 24, 16, 26, 29, 88434)),
        ),
        migrations.AlterField(
            model_name='onlinesupport',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.task'),
        ),
        migrations.AlterField(
            model_name='troubleshoot',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.task'),
        ),
    ]