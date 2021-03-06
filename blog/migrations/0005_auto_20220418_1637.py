# Generated by Django 3.2.12 on 2022-04-18 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_panel', '0025_auto_20220418_1519'),
        ('blog', '0004_blogentry_league'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogentry',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blogentry',
            name='team',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_panel.teams'),
        ),
    ]
