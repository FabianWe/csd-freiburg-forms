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

from .forms import RegisterGeneralForm, VehicleForm, WalkingGroupForm, BoothForm, ConfirmForm
from .models import Applicant, VehicleRegistration, WalkingGroupRegistration, InfoBoothRegistration

from formtools.wizard.views import SessionWizardView, CookieWizardView

REGISTER_FORMS = [
    RegisterGeneralForm,
    VehicleForm,
    WalkingGroupForm,
    BoothForm,
    ConfirmForm,
]

REGISTER_TEMPLATES = {
    '0': 'csd_fr_registration/register_general.html',
    '1': 'csd_fr_registration/register_vehicle.html',
    '2': 'csd_fr_registration/register_walking_group.html',
    '3': 'csd_fr_registration/register_info_booth.html',
    '4': 'csd_fr_registration/register_confirm.html',
}


def get_do_register(wizard, field_name):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {field_name: False}
    return cleaned_data[field_name]

def do_vehicle(wizard):
    return get_do_register(wizard, 'register_vehicle')


def do_walking_group(wizard):
    return get_do_register(wizard, 'register_walking_group')

def do_info_booth(wizard):
    return get_do_register(wizard, 'register_info_booth')

class RegisterWizard(SessionWizardView):
    form_list = REGISTER_FORMS
    condition_dict = {'1': do_vehicle, '2': do_walking_group, '3': do_info_booth}


    def get_template_names(self):
        return [REGISTER_TEMPLATES[self.steps.current]]


    def done(self, form_list, **kwargs):
        data = [form.cleaned_data for form in form_list]
        
        return HttpResponse('JO')

class RegisterGenerelView16(FormView):
    model = Applicant
    form_class = RegisterGeneralForm
    template_name = "csd_fr_registration/register_general.html"

    def form_valid(self, form):
        form.save()
        return HttpResponse('JO')


class VehicleView16(FormView):
    model = VehicleRegistration
    form_class = VehicleForm
    template_name = "csd_fr_registration/register_general.html"

    def form_valid(self, form):
        form.save()
        return HttpResponse('JO')


class WalkingGroupView16(FormView):
    model = WalkingGroupRegistration
    form_class = WalkingGroupForm
    template_name = "csd_fr_registration/register_general.html"

    def form_valid(self, form):
        form.save()
        return HttpResponse('JO')


class BoothView16(FormView):
    model = InfoBoothRegistration
    form_class = BoothForm
    template_name = "csd_fr_registration/register_general.html"

    def form_valid(self, form):
        form.save()
        return HttpResponse('JO')
