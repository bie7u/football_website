# Generated by Django 3.2.12 on 2022-04-17 09:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0023_actualmatchs_today_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actualmatchs',
            name='day',
            field=models.DateField(default=datetime.date(2022, 4, 17)),
        ),
        migrations.AlterField(
            model_name='matchs',
            name='day',
            field=models.DateField(default=datetime.date(2022, 4, 17)),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='date_of_creation',
            field=models.DateField(default=datetime.date(2022, 4, 17)),
        ),
    ]
