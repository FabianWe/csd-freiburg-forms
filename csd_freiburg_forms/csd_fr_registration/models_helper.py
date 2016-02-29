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


def _get_car_prize(pt, is_association):
    if is_association:
        return pt.car_queer_txt, pt.car_queer, pt.car_queer_tax
    else:
        return pt.car_other_txt, pt.car_other, pt.car_other_tax


def _get_truck_prize(pt, is_association):
    if is_association:
        return pt.truck_queer_txt, pt.truck_queer, pt.truck_queer_tax
    else:
        return pt.truck_other_txt, pt.truck_other, pt.truck_other_tax


def _get_vehicle_prize(pt, is_car, is_association):
    if is_car:
        return _get_car_prize(pt, is_association)
    else:
        return _get_truck_prize(pt, is_association)


def _get_walking_group_prize(pt, music, is_association):
    if music:
        return pt.walking_group_music_txt, pt.walking_group_music, pt.walking_group_music_tax
    else:
        return pt.walking_group_no_music_txt, pt.walking_group_no_music, pt.walking_group_no_music_tax


def _get_booth_prize(pt, is_association):
    if is_association:
        return pt.info_booth_queer_txt, pt.info_booth_queer, pt.info_booth_queer_tax
    else:
        return pt.info_booth_other_txt, pt.info_booth_other, pt.info_booth_other_tax
