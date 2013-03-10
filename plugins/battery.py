"""Copyright 2013 by Scott Hansen <firecat4153 @gmail.com

This file is part of py-multistatus.

Py-multistatus is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

Py-multistatus is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
Py-multistatus.  If not, see <http://www.gnu.org/licenses/>.

"""
from .worker import Worker


class PluginBattery(Worker):
    """Display current battery/AC status

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)

    def _update_data(self):
        with open(self.cfg.battery.batt_status) as f:
            status = f.readline().strip()
        with open(self.cfg.battery.batt_charge) as f:
            capacity = "{}%".format(f.readline().strip())
        if status == "Discharging" and int(capacity.strip('%')) > 10:
            out = self._color_text(capacity, fg="black", bg="yellow")
        elif int(capacity.strip('%')) < 10:
            out = self._err_text(capacity)
        else:
            out = self._color_text(capacity, fg="yellow")
        return (self.__qualname__, ":: {} ".format(out))
