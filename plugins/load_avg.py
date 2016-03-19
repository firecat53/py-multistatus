import psutil
from .worker import Worker


class PluginLoadAvg(Worker):
    """Display system load average.

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)

    def _update_data(self):
        lavg = ["{:0.2f}".format(i) for i in psutil.os.getloadavg()]
        out = self.cfg.load_avg.icon
        for i in lavg:
            out += " "
            if float(i) > 1:
                out += self._color_text(i, fg=self.cfg.load_avg.color_bg,
                                        bg=self.cfg.load_avg.color_fg)
            else:
                out += self._color_text(i, fg=self.cfg.load_avg.color_fg)
        return (self.__module__, self._out_format(out))
