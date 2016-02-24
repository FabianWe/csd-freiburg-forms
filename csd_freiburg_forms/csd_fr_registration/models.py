# Copyright (C) 2016 Fabian Wenzelmann
#
# This file is part of csd-freiburg-forms.
#
# csd-freiburg-forms is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# csd-freiburg-forms is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with csd-freiburg-forms. If not, see <http://www.gnu.org/licenses/>.
#

from django.db import models
import django.utils
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

# Create your models here.


class RegistrationCost(models.Model):
    year = models.PositiveIntegerField(
        _('Jahr'),
        help_text=_('Jahr (4-stellig)'),
        primary_key=True)
    car_queer = models.PositiveIntegerField(
        _('Preis Auto queere Gruppen'))
    car_other = models.PositiveIntegerField(
        _('Preis Auto Sonstige'))
    truck_queer = models.PositiveIntegerField(
        _('Preis LKW queere Gruppen'))
    truck_other = models.PositiveIntegerField(
        _('Preis LKW Sonstige'))
    walking_group_no_music = models.PositiveIntegerField(
        _('Preis Fußgruppen ohne Musik'))
    walking_group_music = models.PositiveIntegerField(
        _('Preis Fußgruppen mit Musik'))
    info_booth_queer = models.PositiveIntegerField(
        _('Preis Infostand queere Gruppen'))
    info_booth_other = models.PositiveIntegerField(
        _('Preis Infostand Sonstige'))

class Applicant(models.Model):
    organisation = models.CharField(
        _('Organisation'),
        help_text=_('Name der Organisation'),
        max_length=100)
    is_association = models.BooleanField(
        _('queerer* Verein'),
        help_text=_('Handelt es sich um einen explizit queeren* Verein / Projekt / Gruppe (keine Unternehmen!)'))
    person_responsible = models.CharField(
        _('Verantwortliche*r'),
        help_text=_('Name der Person, die verantwortlich ist'),
        max_length=100)
    street = models.CharField(
        _('Straße'),
        help_text=_('Straße und Hausnummer'),
        max_length=100)
    zip_code = models.CharField(
        _('PLZ'),
        help_text=_('Postleitzahl'),
        max_length=5)
    city = models.CharField(_('Ort'), help_text=_('Ort'), max_length=100)
    phone = models.CharField(
        _('Telefon'),
        help_text=_('Telefonnummer'),
        max_length=20)
    mail = models.EmailField(
        _('E-Mail'),
        help_text=_('E-Mail für weiteren Kontakt'))
    year = models.PositiveIntegerField(
        _('Jahr'),
        help_text=_('Jahr (4-stellig)'))


class ApplicantPosted(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    posted_time = models.DateTimeField(_('Date published'), default=django.utils.timezone.now)

class GeneralRegistration(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)

class VehicleRegistration(GeneralRegistration):
    is_car = models.BooleanField(
        _('Auto?'),
        help_text=_('Handelt es sich um einen PKW?'))
    size = models.CharField(
        _('Größe'),
        help_text=_('Größe des Wagens, L x B x H in cm'),
        max_length=100)
    equipment = models.CharField(
        _('Technische Ausstattung'),
        help_text=_('Technische Ausstattung, z.B. Anlagen, Generatoren'),
        max_length=500,
        blank=True)
    show = models.TextField(
        _('Programm'),
        help_text=_(
            'Artists, Musikgenre, Performances; kurz  zusammengefasst'),
        max_length=500,
        blank=True)
    decoration = models.TextField(
        _('Deko'),
        help_text=_('Falls ihr schon Ideen zur Dekoration habt'),
        max_length=500,
        blank=True)
    notes = models.TextField(
        _('Sonstiges'),
        help_text=_('Sonstige Anmerkungen'),
        max_length=500,
        blank=True)


class WalkingGroupRegistration(GeneralRegistration):
    people = models.PositiveIntegerField(
        _('Teilnehmer*innen Anzahl'),
        help_text=_('Ungefähre Anzahl der Teilnehmer*innen'))
    show = models.TextField(
        _('Programm'),
        help_text=_(
            'Artists, Musikgenre, Performances; kurz  zusammengefasst'),
        max_length=500,
        blank=True)
    music = models.BooleanField(
        _('Musik'),
        help_text=_('Wird Musik gespielt?'))
    notes = models.TextField(
        _('Sonstiges'),
        help_text=_('Sonstige Anmerkungen'),
        max_length=500,
        blank=True)


class InfoBoothRegistration(GeneralRegistration):
    subject = models.CharField(
        _('Thema'),
        help_text=_('Thema des Standes'),
        max_length=500)
    size = models.CharField(
        _('Größe'),
        help_text=_('Größe des Standes, L x B in cm'),
        max_length=100)
    notes = models.TextField(
        _('Sonstiges'),
        help_text=_('Sonstige Anmerkungen'),
        max_length=500,
        blank=True)
