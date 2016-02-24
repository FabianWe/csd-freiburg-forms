# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 05:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation', models.CharField(help_text='Name der Organisation', max_length=100, verbose_name='Organisation')),
                ('is_association', models.BooleanField(help_text='Handelt es sich um einen explizit queeren* Verein / Projekt / Gruppe (keine Unternehmen!)', verbose_name='queerer* Verein')),
                ('person_responsible', models.CharField(help_text='Name der Person, die verantwortlich ist', max_length=100, verbose_name='Verantwortliche*r')),
                ('street', models.CharField(help_text='Straße und Hausnummer', max_length=100, verbose_name='Straße')),
                ('zip_code', models.CharField(help_text='Postleitzahl', max_length=5, verbose_name='PLZ')),
                ('city', models.CharField(help_text='Ort', max_length=100, verbose_name='Ort')),
                ('phone', models.CharField(help_text='Telefonnummer', max_length=20, verbose_name='Telefon')),
                ('mail', models.EmailField(help_text='E-Mail für weiteren Kontakt', max_length=254, verbose_name='E-Mail')),
                ('year', models.PositiveIntegerField(help_text='Jahr (4-stellig)', verbose_name='Jahr')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicantPosted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date published')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csd_fr_registration.Applicant')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationCost',
            fields=[
                ('year', models.PositiveIntegerField(help_text='Jahr (4-stellig)', primary_key=True, serialize=False, verbose_name='Jahr')),
                ('car_queer', models.PositiveIntegerField(verbose_name='Preis Auto queere Gruppen')),
                ('car_other', models.PositiveIntegerField(verbose_name='Preis Auto Sonstige')),
                ('truck_queer', models.PositiveIntegerField(verbose_name='Preis LKW queere Gruppen')),
                ('truck_other', models.PositiveIntegerField(verbose_name='Preis LKW Sonstige')),
                ('walking_group_no_music', models.PositiveIntegerField(verbose_name='Preis Fußgruppen ohne Musik')),
                ('walking_group_music', models.PositiveIntegerField(verbose_name='Preis Fußgruppen mit Musik')),
                ('info_booth_queer', models.PositiveIntegerField(verbose_name='Preis Infostand queere Gruppen')),
                ('info_booth_other', models.PositiveIntegerField(verbose_name='Preis Infostand Sonstige')),
            ],
        ),
        migrations.CreateModel(
            name='InfoBoothRegistration',
            fields=[
                ('generalregistration_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='csd_fr_registration.GeneralRegistration')),
                ('subject', models.CharField(help_text='Thema des Standes', max_length=500, verbose_name='Thema')),
                ('size', models.CharField(help_text='Größe des Standes, L x B in cm', max_length=100, verbose_name='Größe')),
                ('notes', models.TextField(blank=True, help_text='Sonstige Anmerkungen', max_length=500, verbose_name='Sonstiges')),
            ],
            bases=('csd_fr_registration.generalregistration',),
        ),
        migrations.CreateModel(
            name='VehicleRegistration',
            fields=[
                ('generalregistration_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='csd_fr_registration.GeneralRegistration')),
                ('is_car', models.BooleanField(help_text='Handelt es sich um einen PKW?', verbose_name='Auto?')),
                ('size', models.CharField(help_text='Größe des Wagens, L x B x H in cm', max_length=100, verbose_name='Größe')),
                ('equipment', models.CharField(blank=True, help_text='Technische Ausstattung, z.B. Anlagen, Generatoren', max_length=500, verbose_name='Technische Ausstattung')),
                ('show', models.TextField(blank=True, help_text='Artists, Musikgenre, Performances; kurz  zusammengefasst', max_length=500, verbose_name='Programm')),
                ('decoration', models.TextField(blank=True, help_text='Falls ihr schon Ideen zur Dekoration habt', max_length=500, verbose_name='Deko')),
                ('notes', models.TextField(blank=True, help_text='Sonstige Anmerkungen', max_length=500, verbose_name='Sonstiges')),
            ],
            bases=('csd_fr_registration.generalregistration',),
        ),
        migrations.CreateModel(
            name='WalkingGroupRegistration',
            fields=[
                ('generalregistration_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='csd_fr_registration.GeneralRegistration')),
                ('people', models.PositiveIntegerField(help_text='Ungefähre Anzahl der Teilnehmer*innen', verbose_name='Teilnehmer*innen Anzahl')),
                ('show', models.TextField(blank=True, help_text='Artists, Musikgenre, Performances; kurz  zusammengefasst', max_length=500, verbose_name='Programm')),
                ('music', models.BooleanField(help_text='Wird Musik gespielt?', verbose_name='Musik')),
                ('notes', models.TextField(blank=True, help_text='Sonstige Anmerkungen', max_length=500, verbose_name='Sonstiges')),
            ],
            bases=('csd_fr_registration.generalregistration',),
        ),
        migrations.AddField(
            model_name='generalregistration',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csd_fr_registration.Applicant'),
        ),
    ]
