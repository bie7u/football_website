# Generated by Django 3.2.12 on 2022-04-21 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0028_auto_20220421_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='infoAboutRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(blank=True, default='', max_length=200)),
                ('league', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user_panel.league')),
                ('round', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user_panel.round')),
                ('season', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user_panel.actualseason')),
            ],
        ),
    ]
