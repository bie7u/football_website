# Generated by Django 3.2.12 on 2022-04-21 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0031_infoaboutleague'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infoaboutleague',
            name='season',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user_panel.season'),
        ),
    ]