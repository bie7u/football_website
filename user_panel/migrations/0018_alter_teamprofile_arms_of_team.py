# Generated by Django 4.0.3 on 2022-04-02 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0017_alter_teamprofile_arms_of_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamprofile',
            name='arms_of_team',
            field=models.ImageField(blank=True, default='images/default_arms.png', null=True, upload_to='images/'),
        ),
    ]
