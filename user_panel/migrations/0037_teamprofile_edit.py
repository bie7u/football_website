# Generated by Django 3.2.12 on 2022-04-24 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0036_teamprofile_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamprofile',
            name='edit',
            field=models.BooleanField(default=False),
        ),
    ]
