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

from django.template.defaulttags import register


@register.filter
def format_euro(val):
    str_ = str(val)
    if len(str_) == 1:
        return '0,0' + str_ + ' €'
    elif len(str_) == 2:
        return '0,' + str_ + ' €'
    euro, cent = str_[:-2], str_[-2:]
    return euro + ',' + cent + ' €'


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)
