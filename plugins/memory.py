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
from psutil import virtual_memory


class PluginMemory(Worker):
    """Display memory usage percent

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)
        self.high_alert = int(self.cfg.memory.high_alert)
        self.high_warn = int(self.cfg.memory.high_warn)

    def _update_data(self):
        mem = int(virtual_memory().percent)
        out = "{} {}%".format(self.cfg.memory.icon, str(mem))
        if mem > self.high_alert:
            out = self._err_text(out)
        elif mem > self.high_warn:
            out = self._color_text(out, fg=self.cfg.memory.color_bg,
                                   bg=self.cfg.memory.color_fg)
        elif self.cfg.memory.show_always == 'True':
            out = self._color_text(out, fg=self.cfg.memory.color_fg,
                                   bg=self.cfg.memory.color_bg)
        else:
            out = ""
        return (self.__module__, self._out_format(out))
