#!/usr/bin/env python

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

from collections import OrderedDict
from subprocess import Popen, PIPE

import plugins
from lib import config

# TODO Configuration file?
# TODO network speed
# TODO put in initial data for instant display on start
# TODO music display
# TODO move weather.sh from crontab into here?

sections = "{} {} {}".format(config.general.left,
                             config.general.center,
                             config.general.right).split()
# Import only the plugins that are used
plugins.__all__ = sections
from plugins import *

class Statusbar():
    def __init__(self):
        # This whole section is just to initialize an OrderedDict with blank
        # values for all the sections, plus the left, center and right symbols
        self.output = OrderedDict()
        lidx = cidx = ridx = 1
        for section in sections:
            cur_plug = getattr(plugins, section)
            cur_cls = [i for i in dir(cur_plug) if i.startswith('Plugin')][0]
            if config.general.left and section in config.general.left and lidx:
                self.output['left'] = config.bar.left_sym
                lidx = 0
            elif config.general.center and section in config.general.center and cidx:
                self.output['center'] = config.bar.center_sym
                cidx = 0
            elif config.general.right and section in config.general.right and ridx:
                self.output['right'] = config.bar.right_sym
                cidx = 0
            self.output[cur_cls] = ""

    def _start_threads(self):
        """Create the queue and start all the desired plugin threads.

        """
        for section in sections:
            args = {"cfg": config,
                    "interval": getattr(getattr(config, section), 'interval')}
            cur_plug = getattr(plugins, section)
            cur_cls = [i for i in dir(cur_plug) if i.startswith('Plugin')][0]
            # Start the thread
            getattr(cur_plug, cur_cls)(**args).start()

    def _write_output(self):
            out = "{}\n".format("".join(self.output.values()))
            self.bar.stdin.write(out.encode())

    def run(self):
        self._start_threads()
        self.bar = Popen(config.general.statusbar, stdin=PIPE)
        while config.queue:
            id, res = config.queue.get()
            self.output[id] = res
            self._write_output()


if __name__ == '__main__':
    Statusbar().run()
