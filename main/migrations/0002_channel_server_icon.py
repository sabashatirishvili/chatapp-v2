# Generated by Django 5.0.6 on 2024-08-28 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='server_icon',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
