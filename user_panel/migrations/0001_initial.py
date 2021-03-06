# Generated by Django 4.0.3 on 2022-03-30 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.FileField(max_length=254, upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Seasons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Matchs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_home_result', models.CharField(blank=True, max_length=10)),
                ('team_versus_result', models.CharField(blank=True, max_length=10)),
                ('date', models.CharField(blank=True, max_length=100)),
                ('league', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user_panel.league')),
                ('round', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user_panel.round')),
                ('season', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user_panel.seasons')),
                ('team_home', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='team_home', to='user_panel.teams')),
                ('team_versus', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='team_versus', to='user_panel.teams')),
            ],
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=300)),
                ('transfer', models.BooleanField(default=False)),
                ('league', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user_panel.league')),
                ('season', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user_panel.seasons')),
            ],
        ),
    ]
