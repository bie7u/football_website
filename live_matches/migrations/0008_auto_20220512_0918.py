# Generated by Django 3.2.12 on 2022-05-12 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0050_auto_20220512_0917'),
        ('live_matches', '0007_editresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editresult',
            name='t_one',
        ),
        migrations.RemoveField(
            model_name='editresult',
            name='t_two',
        ),
        migrations.AddField(
            model_name='editresult',
            name='team_home_sc',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='team_home_sc', to='user_panel.teams'),
        ),
        migrations.AddField(
            model_name='editresult',
            name='team_versus_sc',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='team_versus_sc', to='user_panel.teams'),
        ),
    ]
