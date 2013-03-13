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


class PluginDiskUsage(Worker):
    """Display disk usage for mounted drives if over a certain threshhold.

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)

    def _update_data(self):
        out = []
        mounts = [i.mountpoint for i in psutil.disk_partitions()]
        for disk in mounts:
            use = psutil.disk_usage(disk).percent
            if use > int(self.cfg.disk_usage.disk_use_alert):
                out.append(self._err_text("{} {}% ".format(disk, use)))
            elif use > int(self.cfg.disk_usage.disk_use_warn):
                out.append(self._sel_text("{} {}% ".format(disk, use)))
            elif self.cfg.disk_usage.disk_use_norm == 'True':
                out.append(self._color_text("{} {}% ".format(disk, use),
                                            fg=self.cfg.disk_usage.color_fg,
                                            bg=self.cfg.disk_usage.color_bg))
            else:
                out.append("")

        return (self.__qualname__, self._out_format("".join(out)))
