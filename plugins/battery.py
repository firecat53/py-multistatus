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
            capacity = int(f.readline().strip())
        if status == "Discharging" and capacity > int(self.cfg.battery.warn):
            capacity_str = "{} {}".format(self.cfg.battery.batt_icon,
                                         str(capacity))
            out = self._color_text(capacity_str, fg=self.cfg.battery.color_fg)
        elif status == "Discharging" and capacity > int(self.cfg.battery.low):
            capacity_str = "{} {}".format(self.cfg.battery.batt_icon,
                                         str(capacity))
            out = self._color_text(capacity_str, fg=self.cfg.battery.color_bg,
                                   bg=self.cfg.battery.color_fg)
        elif status == "Discharging" and capacity <= int(self.cfg.battery.low):
            capacity_str = "{} {}".format(self.cfg.battery.batt_icon,
                                          str(capacity))
            out = self._err_text(capacity_str)
        else:
            capacity_str = "{} {}".format(self.cfg.battery.ac_icon,
                                         str(capacity))
            out = self._color_text(capacity_str, fg=self.cfg.battery.color_fg,
                                   bg=self.cfg.battery.color_bg)
        return (self.__qualname__, self._out_format(out))
