# Generated by Django 3.2.12 on 2022-04-20 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_blogentry_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogentry',
            name='article_type',
            field=models.CharField(choices=[('1', 'artykul sponsorowany'), ('2', 'artykul nie sponsorowany')], default='2', max_length=100, null=True),
        ),
    ]