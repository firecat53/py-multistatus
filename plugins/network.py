from .worker import Worker
from psutil import net_io_counters
from subprocess import Popen, PIPE
import socket


class PluginNetwork(Worker):
    """New plugin

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)
        self.old = net_io_counters(pernic=True)
        interfaces = self.cfg.network.interfaces.split()
        iface_icons = self.cfg.network.iface_icons.split()
        self.interfaces = dict(zip(interfaces, iface_icons))

    def _round(self, x, base=5):
        """Round number to nearest 10

        """
        return int(base * round(float(x) / base))

    def _check_net_status(self):
        """Check if network is attached to internet.

        """
        try:
            # see if we can resolve the host name -- tells us if there is
            # a DNS listening
            host = socket.gethostbyname(self.cfg.network.url_check)
            # connect to the host -- tells us if the host is actually reachable
            socket.create_connection((host, 80), 2)
            return True
        except:
            # Try both these a second time before calling the network down
            try:
                host = socket.gethostbyname(self.cfg.network.url_check)
                socket.create_connection((host, 80), 2)
                return True
            except:
                pass
        return False

    def _get_interface(self):
        """Determine which of the given interfaces is currently up.

        """
        res = Popen(["ip", "addr"],
                    stdout=PIPE).communicate()[0].decode().split('\n')
        try:
            res = [line for line in res if ' UP ' in line or ',UP,' in line]
            return [i for line in res for i in self.interfaces if i in line][0]
        except IndexError:
            return None

    def _check_vpn(self):
        """Determine if VPN is up or down.

        """
        if Popen(["pgrep", "openvpn"], stdout=PIPE).communicate()[0]:
            return True
        else:
            return False

    def _update_data(self):
        interface = self._get_interface()
        if interface is not None and self._check_net_status() is True:
            self.new = net_io_counters(pernic=True)
            old_down = self.old[interface].bytes_recv
            old_up = self.old[interface].bytes_sent
            new_down = self.new[interface].bytes_recv
            new_up = self.new[interface].bytes_sent
            up = self._round((new_up - old_up) /
                             (1024 * int(self.cfg.network.interval)))
            down = self._round((new_down - old_down) /
                               (1024 * int(self.cfg.network.interval)))
            self.old = self.new
            net_str = "{} {}{:.0f} {}{:.0f}".format(self.interfaces[interface],
                                                    self.cfg.network.up_icon,
                                                    up,
                                                    self.cfg.network.down_icon,
                                                    down)
            if self._check_vpn():
                out = self._color_text(net_str,
                                       fg=self.cfg.network.color_vpn_fg,
                                       bg=self.cfg.network.color_vpn_bg)
            else:
                out = net_str
        else:
            out = self._err_text("Network Down")

        return (self.__module__, self._out_format(out))
