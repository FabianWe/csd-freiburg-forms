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

from .models import Applicant
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

class RegisterGeneralForm(forms.ModelForm):
    register_vehicle = forms.BooleanField(label=_('Wagen anmelden?'))
    register_walking_group = forms.BooleanField(label=_('Fußgruppe anmelden?'))
    register_info_booth = forms.BooleanField(label=_('Infostand anmelden?'))

    class Meta:
        model = Applicant
        exclude = []
