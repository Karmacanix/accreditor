# Generated by Django 2.0.7 on 2018-07-18 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0003_catmeeting_agenda_item_apps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catmeeting',
            name='agenda_item_apps',
        ),
    ]
