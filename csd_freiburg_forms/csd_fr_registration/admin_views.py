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

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from .models import Applicant, ApplicantPosted, VehicleRegistration, WalkingGroupRegistration, InfoBoothRegistration

def _get_year(year):
    if len(year) == 2:
        year = '20' + year
    return int(year)

# we haven't defined the *Registration models not as 1:1, but however they are...
# this helper method adds to registration object to the dictionary if the
# registration exists
def _get_registration(registration_class, attr_name, applicant, applicant_data):
    registration = registration_class.objects.filter(applicant=applicant)
    if registration:
        registration = registration[0]
        applicant_data[attr_name] = registration

@staff_member_required
def year_detail(request, year):
    year = _get_year(year)
    # get all registrations for the given year
    posted_objects = ApplicantPosted.objects.filter(applicant__year=2016).order_by('posted_time')
    result = []
    for posted in posted_objects:
        applicant = posted.applicant
        applicant_data = {'applicant': applicant}
        applicant_data['posted'] = posted
        # get all registrations
        _get_registration(VehicleRegistration, 'vehicle_registration', applicant, applicant_data)
        _get_registration(WalkingGroupRegistration, 'walking_registration', applicant, applicant_data)
        _get_registration(InfoBoothRegistration, 'booth_registration', applicant, applicant_data)
        result.append(applicant_data)
    context = {'year': year, 'applicants': result}
    return render(request, 'admin/csd_fr_registration/year_detail.html', context)

def _get_all_from_type(registration_class, applicant):
    # get all applicants from this year
    return registration_class.objects.filter(applicant=applicant)

@staff_member_required
def year_types(request, year):
    year = _get_year(year)
    posted_objects = ApplicantPosted.objects.filter(applicant__year=2016).order_by('posted_time')
    vehicles = []
    walkings = []
    booths = []
    for posted in posted_objects:
        applicant = posted.applicant
        # get all vehicles
        vehicles += list(_get_all_from_type(VehicleRegistration, applicant))
        walkings += list(_get_all_from_type(WalkingGroupRegistration, applicant))
        booths += list(_get_all_from_type(InfoBoothRegistration, applicant))
    context = {'year': year, 'vehicles': vehicles, 'walkings': walkings, 'booths': booths}
    return render(request, 'admin/csd_fr_registration/year_types.html', context)
