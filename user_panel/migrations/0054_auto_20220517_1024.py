# Generated by Django 3.2.12 on 2022-05-17 08:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0053_auto_20220513_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actualmatchs',
            name='day',
            field=models.DateField(default=datetime.date(2022, 5, 17)),
        ),
        migrations.AlterField(
            model_name='matchs',
            name='day',
            field=models.DateField(default=datetime.date(2022, 5, 17)),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='date_of_creation',
            field=models.DateField(default=datetime.date(2022, 5, 17)),
        ),
    ]
