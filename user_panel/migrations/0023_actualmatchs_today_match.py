# Generated by Django 3.2.12 on 2022-04-07 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0022_alter_actualmatchs_day_alter_actualmatchs_match_info_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='actualmatchs',
            name='today_match',
            field=models.BooleanField(default=False),
        ),
    ]
