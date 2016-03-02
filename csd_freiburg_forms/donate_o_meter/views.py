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

from PIL import Image
import os.path

from django.shortcuts import render
from django.http import HttpResponse, Http404

from .donate_o_meter import DonateOMeter
from .models import DonateAim

# Create your views here.
def meter16(request):
    dir_ = os.path.dirname(os.path.realpath(__file__))
    imgs = os.path.join(dir_, 'imgs')
    empty_path = os.path.join(imgs, 'sektglas.png')
    full_path = os.path.join(imgs, 'sektglas-voll.png')
    empty = Image.open(empty_path)
    full = Image.open(full_path)
    aim = None
    try:
        aim = DonateAim.objects.get(pk=2016)
    except DonateAim.DoesNotExist as e:
        raise Http404('No DonateAim for 2016')
    box = 24, 0, 176, 332
    meter = DonateOMeter(empty, full, aim.aim, box=box)
    img = meter.draw(aim.current)
    response = HttpResponse(content_type='image/png')
    img.save(response, 'PNG')
    return response
