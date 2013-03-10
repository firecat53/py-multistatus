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

#locations = ("/usr/share/py-multistatus", expanduser("~/.config/multistatus"))
locations = ("./",)
parse = ConfigParser()
parse.read([join(i, 'status.cfg') for i in locations])

queue = Queue()

this = modules[__name__]
# (section, <items>)
for sec, item in parse.items():
    nt = namedtuple("nt", item)
    if sec != "DEFAULT":
        setattr(this, sec, nt._make(parse[sec].values()))
