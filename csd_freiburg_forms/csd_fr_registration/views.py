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
from .models import Applicant, VehicleRegistration, WalkingGroupRegistration, InfoBoothRegistration, ApplicantPosted, RegistrationCost
from . import filters

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
    condition_dict = {
        '1': do_vehicle,
        '2': do_walking_group,
        '3': do_info_booth}

    def get_template_names(self):
        return [REGISTER_TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(
            RegisterWizard,
            self).get_context_data(
            form=form,
            **kwargs)
        if self.steps.current == '4':
            articles = []
            amount = 0
            tax_sum = 0
            for article, net, tax in self._get_articles():
                articles.append((article, net, tax, net + tax))
                amount += net
                tax_sum += tax
            context.update(
                {'articles': articles,
                 'net_sum': amount,
                 'tax_sum': tax_sum,
                 'gross_sum': amount + tax_sum,
                 'tax_string': self.get_tax_string()})
        return context

    def _get_is_association(self):
        cleaned_data = self.get_cleaned_data_for_step(
            '0') or {'is_association': False}
        return cleaned_data['is_association']

    def _get_is_car(self):
        cleaned_data = self.get_cleaned_data_for_step('1') or {'is_car': False}
        return cleaned_data['is_car']

    def _get_is_music(self):
        cleaned_data = self.get_cleaned_data_for_step('2') or {'music': False}
        return cleaned_data['music']

    def _get_articles(self):
        is_association = self._get_is_association()
        prizing_table = self._get_prizing_table()
        if do_vehicle(self):
            is_car = self._get_is_car()
            yield self._get_vehicle_prize(
                prizing_table, is_car, is_association)
        if do_walking_group(self):
            music = self._get_is_music()
            yield self._get_walking_group_prize(
                prizing_table, music, is_association)
        if do_info_booth(self):
            yield self._get_booth_prize(
                prizing_table, is_association)

    def _get_prizing_table(self):
        year = self.get_year()
        return RegistrationCost.objects.get(pk=year)

    def _get_car_prize(self, pt, is_association):
        if is_association:
            return pt.car_queer_txt, pt.car_queer, pt.car_queer_tax
        else:
            return pt.car_other_txt, pt.car_other, pt.car_other_tax

    def _get_truck_prize(self, pt, is_association):
        if is_association:
            return pt.truck_queer_txt, pt.truck_queer, pt.truck_queer_tax
        else:
            return pt.truck_other_txt, pt.truck_other, pt.truck_other_tax

    def _get_vehicle_prize(self, pt, is_car, is_association):
        if is_car:
            return self._get_car_prize(pt, is_association)
        else:
            return self._get_truck_prize(pt, is_association)

    def _get_walking_group_prize(self, pt, music, is_association):
        if music:
            return pt.walking_group_music_txt, pt.walking_group_music, pt.walking_group_music_tax
        else:
            return pt.walking_group_no_music_txt, pt.walking_group_no_music, pt.walking_group_no_music_tax

    def _get_booth_prize(self, pt, is_association):
        if is_association:
            return pt.info_booth_queer_txt, pt.info_booth_queer, pt.info_booth_queer_tax
        else:
            return pt.info_booth_other_txt, pt.info_booth_other, pt.info_booth_other_tax

    def done(self, form_list, **kwargs):
        forms = list(form_list)
        data = [form.cleaned_data for form in forms]
        applicant = self._create_applicant(forms[0])
        nxt_form = 1
        if do_vehicle(self):
            vehicle_form = forms[nxt_form]
            nxt_form += 1
            vehicle = self._create_registration(vehicle_form, applicant)
        if do_walking_group(self):
            walking_form = forms[nxt_form]
            nxt_form += 1
            walking = self._create_registration(walking_form, applicant)
        if do_info_booth(self):
            booth_form = forms[nxt_form]
            nxt_form += 1
            booth = self._create_registration(booth_form, applicant)
        accept_form = forms[nxt_form]
        accept_data = self.get_context_data(accept_form)
        net_sum, tax, gross = accept_data['net_sum'], accept_data['tax_sum'], accept_data['gross_sum']
        self._create_posted(applicant, net_sum, tax, gross)
        return HttpResponse('JO')

    def _create_applicant(self, form):
        applicant = form.save(commit=False)
        applicant.year = self.get_year()
        applicant.save()
        form.save_m2m()
        return applicant

    def _create_registration(self, form, applicant):
        obj = form.save(commit=False)
        obj.applicant = applicant
        obj.save()
        form.save_m2m()
        return obj

    def _create_posted(self, applicant, net_sum, tax, gross):
        posted = ApplicantPosted(applicant=applicant, net=net_sum, tax=tax, gross=gross)
        posted.save()


class RegisterWizard16(RegisterWizard):

    def get_year(self):
        return 2016

    def get_tax_string(self):
        return 'USt. 19%'


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
