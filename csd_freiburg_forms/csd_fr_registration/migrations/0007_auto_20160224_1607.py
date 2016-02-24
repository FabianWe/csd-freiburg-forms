# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 16:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csd_fr_registration', '0006_auto_20160224_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicantposted',
            name='id',
        ),
        migrations.AlterField(
            model_name='applicantposted',
            name='applicant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='csd_fr_registration.Applicant'),
        ),
    ]
