# Generated by Django 3.2.12 on 2022-04-24 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0047_remove_teamprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamprofile',
            name='user',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
