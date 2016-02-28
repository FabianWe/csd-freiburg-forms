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
    if len(year) == 2:
        year = '20' + year
    year = int(year)
    # get all registrations for the given year
    applicants = Applicant.objects.filter(year=year)
    result = []
    for applicant in applicants:
        applicant_data = {'applicant': applicant}
        # get ApplicantPosted information
        posted = ApplicantPosted.objects.get(applicant=applicant)
        applicant_data['posted'] = posted
        # get all registrations
        _get_registration(VehicleRegistration, 'vehicle_registration', applicant, applicant_data)
        _get_registration(WalkingGroupRegistration, 'walking_registration', applicant, applicant_data)
        _get_registration(InfoBoothRegistration, 'boot_registration', applicant, applicant_data)
        result.append(applicant_data)
    context = {'year': year, 'applicants': result}
    return render(request, 'admin/csd_fr_registration/year_detail.html', context)
