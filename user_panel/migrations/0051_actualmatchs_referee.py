# Generated by Django 3.2.12 on 2022-05-12 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0050_auto_20220512_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='actualmatchs',
            name='referee',
            field=models.CharField(blank=True, default='Nie podano sędziego', max_length=50, null=True),
        ),
    ]