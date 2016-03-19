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
from subprocess import Popen, PIPE
from .worker import Worker


class PluginDate(Worker):
    """Display current Watson (http://tailordev.github.io/Watson/) project

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)

    def _update_data(self):
        res = Popen(["watson", "status"], stdout=PIPE).communicate()[0]
        res = res.decode()
        if not res.startswith("No project started"):
            out = self._color_text(res.split()[1].strip(),
                                   fg=self.cfg.watson.color_fg,
                                   bg=self.cfg.watson.color_bg)
        else:
            out = ""
        return (self.__module__, self._out_format(out))
