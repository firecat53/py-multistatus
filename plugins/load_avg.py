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
import psutil
from .worker import Worker


class PluginLoadAvg(Worker):
    """Display system load average.

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)

    def _update_data(self):
        lavg = ["{:0.2f}".format(i) for i in psutil.os.getloadavg()]
        out = "{} {}".format(self.cfg.load_avg.icon, " ".join(lavg))
        out = self._color_text(out, fg=self.cfg.load_avg.color_fg)
        return (self.__qualname__, self._out_format(out))
