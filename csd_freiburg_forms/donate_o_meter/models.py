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

from django.db import models
import django.utils
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

# Create your models here.
class DonateAim(models.Model):
    year = models.PositiveIntegerField(
        _('Jahr'),
        help_text=_('Jahr (4-stellig)'),
        primary_key=True)
    aim = models.PositiveIntegerField(
        _('Spendenziel'),
        help_text=_('Spendenziel in Cent'))
    current = models.PositiveIntegerField(
        _('Aktuell'),
        help_text=_('Aktueller Stand in Cent'),
        default=0)
