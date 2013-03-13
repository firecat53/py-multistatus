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
from collections import namedtuple
from configparser import ConfigParser
from os.path import expanduser, join
from queue import Queue
from sys import modules

locations = ("/usr/share/py-multistatus",
             expanduser("~/.local/share/py-multistatus"),
             expanduser("~/.config/py-multistatus"))
parse = ConfigParser()
parse.read([join(i, 'status.cfg') for i in locations])

queue = Queue()

this = modules[__name__]
# (section, <items>)
for sec, item in parse.items():
    nt = namedtuple("nt", item)
    if sec != "DEFAULT":
        setattr(this, sec, nt._make(parse[sec].values()))

# Set some bar color attributes
bar = bar._replace(norm_fg="{}{}".format(bar.fg_sym, getattr(bar, bar.norm_fg)))
bar = bar._replace(norm_bg="{}{}".format(bar.bg_sym, getattr(bar, bar.norm_bg)))
bar = bar._replace(sel_fg="{}{}".format(bar.fg_sym, getattr(bar, bar.sel_fg)))
bar = bar._replace(sel_bg="{}{}".format(bar.bg_sym, getattr(bar, bar.sel_bg)))
bar = bar._replace(err_fg="{}{}".format(bar.fg_sym, getattr(bar, bar.err_fg)))
bar = bar._replace(err_bg="{}{}".format(bar.bg_sym, getattr(bar, bar.err_bg)))
bar = bar._replace(sep_fg="{}{}".format(bar.fg_sym, getattr(bar, bar.sep_fg)))
bar = bar._replace(sep_bg="{}{}".format(bar.bg_sym, getattr(bar, bar.sep_bg)))

if bar.sep_space == 'True':
    bar = bar._replace(separator=" {} ".format(bar.separator))

# Color the separator
bar = bar._replace(separator="{}{}{}{}".format(bar.sep_fg,
                                               bar.sep_bg,
                                               bar.separator,
                                               bar.reset_sym))
