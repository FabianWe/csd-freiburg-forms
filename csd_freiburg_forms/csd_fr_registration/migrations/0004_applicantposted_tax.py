# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csd_fr_registration', '0003_auto_20160224_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicantposted',
            name='tax',
            field=models.PositiveIntegerField(default=0, help_text='Steuern für die Anmeldung Anmeldung', verbose_name='Summe der Steuern'),
            preserve_default=False,
        ),
    ]
