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

from django import forms
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

from .models import Applicant, VehicleRegistration, WalkingGroupRegistration, InfoBoothRegistration


class RegisterGeneralForm(forms.ModelForm):
    register_vehicle = forms.BooleanField(label=_('Wagen anmelden?'), required=False)
    register_walking_group = forms.BooleanField(label=_('Fußgruppe anmelden?'), required=False)
    register_info_booth = forms.BooleanField(label=_('Infostand anmelden?'), required=False)

    class Meta:
        model = Applicant
        exclude = ['year']


class VehicleForm(forms.ModelForm):
    class Meta:
        model = VehicleRegistration
        exclude = ['applicant']


class WalkingGroupForm(forms.ModelForm):
    class Meta:
        model = WalkingGroupRegistration
        exclude = ['applicant']


class BoothForm(forms.ModelForm):
    class Meta:
        model = InfoBoothRegistration
        exclude = ['applicant']


class ConfirmForm(forms.Form):
    conditions_of_participation = forms.BooleanField(label=_('Akzeptiere die Teilnahmebedingungen'), required=True)
    # TODO was sonst noch so zu akzeptieren ist
