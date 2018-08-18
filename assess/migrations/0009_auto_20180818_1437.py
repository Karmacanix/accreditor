# Generated by Django 2.0.7 on 2018-08-18 02:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assess', '0008_auto_20180731_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='catmeeting',
            name='apps',
            field=models.ManyToManyField(limit_choices_to={'assess_status': 'A', 'clinical_decision__isnull': False, 'privacy_decision__isnull': False, 'security_decision__isnull': False}, to='assess.Application'),
        ),
        migrations.AlterField(
            model_name='catmeeting',
            name='meeting_date',
            field=models.DateField(default=datetime.date(2018, 8, 18)),
        ),
        migrations.AlterField(
            model_name='cloudquestionnaire',
            name='alteration_risk',
            field=models.BooleanField(default=False, help_text="If the app's information is altered by mistake or intentionally by a wrongdoer, a person(s) or organisation(s) will be harmed.", verbose_name='Information Alteration'),
        ),
        migrations.AlterField(
            model_name='cloudquestionnaire',
            name='continuity_risk',
            field=models.BooleanField(default=False, help_text='If the service is disrupted or is unavailable for an extended, we will be unable to carry out our activities .', verbose_name='Business Continuity'),
        ),
        migrations.AlterField(
            model_name='cloudquestionnaire',
            name='disclosure_risk',
            field=models.BooleanField(default=False, help_text='If a data breach or release of information into the public domain occurred it would compromise our obligations to a person or an organisation.', verbose_name='Privacy Breach'),
        ),
        migrations.AlterField(
            model_name='cloudquestionnaire',
            name='loss_risk',
            field=models.BooleanField(default=False, help_text='If the information is lost by the cloud provider OR we can easily maintain a local copy of the information, a person(s) or orginastion will be harmed.', verbose_name='Data Loss'),
        ),
        migrations.AlterField(
            model_name='historicalinformationclassification',
            name='unclassified',
            field=models.BooleanField(default=False, help_text='All other information. Cannot derive persons identity from data.'),
        ),
        migrations.AlterField(
            model_name='informationclassification',
            name='unclassified',
            field=models.BooleanField(default=False, help_text='All other information. Cannot derive persons identity from data.'),
        ),
    ]
