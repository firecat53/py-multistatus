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
import re
from collections import namedtuple
from .worker import Worker


class PluginMonsterWM(Worker):
    """Parse monsterwm output and create the desktops display.

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)

    def _update_data(self):
        # set values for
        # cm - current monitor??
        # cmi - current monitor index??
        # d - the desktop id
        # w - number of windows in that desktop
        # m - tiling layout/mode for that desktop
        # c - whether that desktop is the current (1) or not (0)
        # u - whether a window in that desktop has an urgent hint set (1) or not (0)
        ## Example: b'0:1:0:1:1:1:0 0:1:1:1:1:0:0 0:1:2:1:1:0:0 0:1:3:0:1:0:0 0:1:4:0:1:0:0 0:1:5:0:1:0:0 0:1:6:0:1:0:0 '

        desks = self.cfg.monsterwm.desks.split()
        modes = self.cfg.monsterwm.modes.split()
        mw = namedtuple("mw", ("cur_mon", "cur_mon_idx", "desk_id", "num_win", "mode", "cur_desk", "urgent"))
        pattern = "^(([0-9]+:){6}[0-9] ?)+$"  # Matches monsterwm output

        with open(self.cfg.monsterwm.fifo, 'r') as f:
            while True:
                res = f.readline()
                r = tm = ""
                match = re.search(pattern, res)
                if match is not None:
                    res = res.strip().split(' ')
                    for desktop in res:
                        desk = mw(*desktop.split(':'))
                        ws = desks[int(desk.desk_id)]  # Set current workspace symbol
                        if int(desk.num_win) > 0:
                            ic = "\u00b0"
                        else:
                            ic = " "
                        if int(desk.cur_desk):  # Reverse back/foreground for current workspace
                            col = self._sel_text
                            # Set current tiling mode
                            tm = self._color_text(modes[int(desk.mode)].format(desk.num_win))
                        else:
                            col = self._color_text
                        if int(desk.urgent):
                            col = self._err_text
                        # active windows icon + workspace icon
                        r += col("{}{} ".format(ic, ws))
                    return (self.__module__, "{} {}".format(r, tm))
