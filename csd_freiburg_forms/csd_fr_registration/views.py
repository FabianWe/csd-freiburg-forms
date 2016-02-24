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

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http import HttpResponse

from .forms import RegisterGeneralForm
from .models import Applicant

class RegisterGenerelView16(FormView):
    model = Applicant
    form_class = RegisterGeneralForm
    template_name = "csd_fr_registration/register_general.html"

    def form_valid(self, form):
        form.save()
        return HttpResponse('JO')
