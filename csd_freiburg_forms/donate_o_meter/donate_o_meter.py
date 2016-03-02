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

class DonateOMeter:

    def __init__(self, background, filling, aim, box=None):
        self.background = background
        self.filling = filling
        self.aim = aim
        if box is None:
            width, height = background.size
            box = (0, 0, width - 1, height - 1)
        self.box = box

    def draw(self, current):
        box = self.box

        # otherwise compute the percent and crop the fill area
        percent = current / self.aim

        width, height = self.background.size
        mh = box[3] - box[1]
        ch = int(mh * percent)
        # first check if ch is zero, in this case return the background
        if ch <= 0:
            return self.background.copy()
        # check if ch is the height of the box, in this case return
        # the filling
        if ch >= (box[3] - box[1]):
            return self.filling.copy()
        img = self.background.copy()
        crop_left = box[0]
        crop_upper = box[3] - ch
        crop_right = box[2]
        crop_lower = box[3]

        # crop the designated area from the image
        meter_area = self.filling.crop(
            (crop_left, crop_upper, crop_right, crop_lower))
        img.paste(meter_area, (crop_left, crop_upper))
        return img
