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
from psutil import network_io_counters
from subprocess import Popen, PIPE
from socket import gethostbyaddr, herror


class PluginNetwork(Worker):
    """New plugin

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)
        self.old = network_io_counters(pernic=True)
        interfaces = self.cfg.network.interfaces.split()
        iface_icons = self.cfg.network.iface_icons.split()
        self.interfaces = dict(zip(interfaces, iface_icons))

    def _round(self, x, base=5):
        """Round number to nearest 10

        """
        return int(base * round(float(x) / base))

    def _check_net_status(self):
        """Check if network is attached to internet by checking ability to
        query google DNS (8.8.8.8)

        """
        try:
            gethostbyaddr('8.8.8.8')
        except herror:
            return False
        else:
            return True

    def _get_interface(self):
        """Determine which of the given interfaces is currently up.

        """
        res = Popen(["ip", "addr"], stdout=PIPE).communicate()[0].decode().split('\n')
        try:
            res = [line for line in res if 'LOOPBACK' not in line and
                   (' UP ' in line or ',UP,' in line)][0]
            return [i for i in self.interfaces if i in res][0]
        except IndexError:
            return None

    def _update_data(self):
        interface = self._get_interface()
        if interface is not None and self._check_net_status() is True:
            self.new = network_io_counters(pernic=True)
            old_down = self.old[interface].bytes_recv
            old_up = self.old[interface].bytes_sent
            new_down = self.new[interface].bytes_recv
            new_up = self.new[interface].bytes_sent
            up = self._round((new_up - old_up) /
                            (1024 * int(self.cfg.network.interval)))
            down = self._round((new_down - old_down) /
                            (1024 * int(self.cfg.network.interval)))
            self.old = self.new
            out = "{} {}{:.0f} {}{:.0f}".format(self.interfaces[interface],
                                               self.cfg.network.up_icon, up,
                                               self.cfg.network.down_icon, down)
        else:
            out = self._err_text("Network Down")

        return (self.__qualname__, self._out_format(out))
