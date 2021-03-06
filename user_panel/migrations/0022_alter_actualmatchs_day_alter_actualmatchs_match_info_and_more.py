# Generated by Django 4.0.3 on 2022-04-06 22:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0021_teamprofile_capitan_teamprofile_chairman_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actualmatchs',
            name='day',
            field=models.DateField(default=datetime.date(2022, 4, 7)),
        ),
        migrations.AlterField(
            model_name='actualmatchs',
            name='match_info',
            field=models.TextField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='matchs',
            name='day',
            field=models.DateField(default=datetime.date(2022, 4, 7)),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='date_of_creation',
            field=models.DateField(default=datetime.date(2022, 4, 7)),
        ),
    ]
