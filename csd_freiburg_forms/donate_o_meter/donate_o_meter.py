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
    def __init__(self, background, filling, aim):
        self.background = background
        self.filling = filling
        self.aim = aim

    def draw(self, current):
        img = self.background.copy()
        percent = current / self.aim
        if percent > 1:
            percent = 1.0
        width, height = self.filling.size
        upper = height - min(int(height * percent), height)
        if upper == height:
            upper -= 1
        box = (0, upper, width, height)
        fill = self.filling.crop(box)
        img.paste(fill, (0, upper))
        return img
