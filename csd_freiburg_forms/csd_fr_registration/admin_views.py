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

import json

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from .models import Applicant, ApplicantPosted, VehicleRegistration, WalkingGroupRegistration, InfoBoothRegistration, RegistrationCost
from .models_helper import _get_vehicle_prize, _get_walking_group_prize, _get_booth_prize


def _get_year(year):
    if len(year) == 2:
        year = '20' + year
    return int(year)

# we haven't defined the Registration models not as 1:1, but however they are...
# this helper method adds to registration object to the dictionary if the
# registration exists


def _get_registration(registration_class, applicant):
    registration = registration_class.objects.filter(applicant=applicant)
    if registration:
        return registration[0]
    else:
        return None


def _add_registration_to_dict(
    registration_class,
    attr_name,
    applicant,
        applicant_data):
    registration = registration_class.objects.filter(applicant=applicant)
    if registration:
        registration = registration[0]
        applicant_data[attr_name] = registration


@staff_member_required
def year_detail(request, year):
    year = _get_year(year)
    # get all registrations for the given year
    posted_objects = ApplicantPosted.objects.filter(
        applicant__year=2016).order_by('posted_time')
    result = []
    for posted in posted_objects:
        applicant = posted.applicant
        applicant_data = {'applicant': applicant}
        applicant_data['posted'] = posted
        # get all registrations
        _add_registration_to_dict(
            VehicleRegistration,
            'vehicle_registration',
            applicant,
            applicant_data)
        _add_registration_to_dict(
            WalkingGroupRegistration,
            'walking_registration',
            applicant,
            applicant_data)
        _add_registration_to_dict(
            InfoBoothRegistration,
            'booth_registration',
            applicant,
            applicant_data)
        result.append(applicant_data)
    context = {'year': year, 'applicants': result}
    return render(request, 'admin/csd_fr_registration/year_detail.html', context)


def _get_all_from_type(registration_class, applicant):
    # get all applicants from this year
    return registration_class.objects.filter(applicant=applicant)


@staff_member_required
def year_types(request, year):
    year = _get_year(year)
    posted_objects = ApplicantPosted.objects.filter(
        applicant__year=2016).order_by('posted_time')
    vehicles = []
    walkings = []
    booths = []
    for posted in posted_objects:
        applicant = posted.applicant
        # get all vehicles
        vehicles += list(_get_all_from_type(VehicleRegistration, applicant))
        walkings += list(
            _get_all_from_type(
                WalkingGroupRegistration,
                applicant))
        booths += list(_get_all_from_type(InfoBoothRegistration, applicant))
    context = {
        'year': year,
        'vehicles': vehicles,
        'walkings': walkings,
        'booths': booths}
    return render(request, 'admin/csd_fr_registration/year_types.html', context)


def _set_invoice_value(dict_, elem, field):
    dict_[field] = getattr(elem, field)


def _get_articles(pt, applicant):
    is_association = applicant.is_association
    names = ['description', 'net', 'tax']
    # first vehicle
    vehicle = _get_registration(VehicleRegistration, applicant)
    if vehicle is not None:
        yield dict(zip(names, _get_vehicle_prize(pt, vehicle.is_car, is_association)))
    walking = _get_registration(WalkingGroupRegistration, applicant)
    if walking is not None:
        yield dict(zip(names, _get_walking_group_prize(pt, walking.music, is_association)))
    booth = _get_registration(InfoBoothRegistration, applicant)
    if booth is not None:
        yield dict(zip(names, _get_booth_prize(pt, is_association)))


@staff_member_required
def json_invoice(request, applicant_id):
    applicant_id = int(applicant_id)
    applicant = None
    try:
        applicant = Applicant.objects.get(pk=applicant_id)
    except Applicant.DoesNotExist as e:
        raise Http404('Invalid id %d' % applicant_id)
    # create result dictionary
    result = {}
    # add all information about the applicant
    _set_invoice_value(result, applicant, 'organisation')
    _set_invoice_value(result, applicant, 'person_responsible')
    _set_invoice_value(result, applicant, 'street')
    _set_invoice_value(result, applicant, 'zip_code')
    _set_invoice_value(result, applicant, 'city')
    # get posted data
    posted = ApplicantPosted.objects.get(pk=applicant)

    # get posted date by hand... json doesn't handle this
    posted_time = posted.posted_time
    date_dict = {
        'day': posted_time.day,
        'month': posted_time.month,
        'year': posted_time.year}
    result['date_posted'] = date_dict
    _set_invoice_value(result, posted, 'net')
    _set_invoice_value(result, posted, 'gross')

    # get the prizing table for this year
    pt = None
    try:
        pt = RegistrationCost.objects.get(pk=applicant.year)
    except RegistrationCost.DoesNotExist as e:
        raise Http404('Invalid year %d' % year)
    articles = list(_get_articles(pt, applicant))
    result['articles'] = articles
    content = json.dumps(result, ensure_ascii=False).encode('utf8')
    response = HttpResponse(content, content_type='application/json')
    response[
        'Content-Disposition'] = 'attachment; filename="invoice_%d.json"' % applicant_id
    return response
