# Generated by Django 2.0.7 on 2018-07-20 12:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0004_remove_catmeeting_agenda_item_apps'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='escalate_IPSG',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalapplication',
            name='escalate_IPSG',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='application',
            name='assess_status',
            field=models.CharField(choices=[('N', 'New'), ('S', 'Submitted'), ('A', 'Assessing'), ('R', 'Rejected'), ('P', 'Approved')], default='N', max_length=1, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='catmeeting',
            name='meeting_date',
            field=models.DateField(default=datetime.date(2018, 7, 21)),
        ),
        migrations.AlterField(
            model_name='historicalapplication',
            name='assess_status',
            field=models.CharField(choices=[('N', 'New'), ('S', 'Submitted'), ('A', 'Assessing'), ('R', 'Rejected'), ('P', 'Approved')], default='N', max_length=1, verbose_name='Status'),
        ),
    ]
