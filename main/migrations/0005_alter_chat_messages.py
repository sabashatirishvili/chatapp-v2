# Generated by Django 5.1 on 2024-09-02 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_channel_owner_alter_channel_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(blank=True, null=True, to='main.message', verbose_name='messages'),
        ),
    ]
