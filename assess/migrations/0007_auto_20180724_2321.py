# Generated by Django 2.0.7 on 2018-07-24 11:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0006_auto_20180722_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catmeeting',
            name='meeting_date',
            field=models.DateField(default=datetime.date(2018, 7, 24)),
        ),
    ]
