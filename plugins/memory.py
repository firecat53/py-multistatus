from .worker import Worker
from psutil import virtual_memory


class PluginMemory(Worker):
    """Display memory usage percent

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)
        self.high_alert = int(self.cfg.memory.high_alert)
        self.high_warn = int(self.cfg.memory.high_warn)

    def _update_data(self):
        mem = int(virtual_memory().percent)
        out = "{} {}%".format(self.cfg.memory.icon, str(mem))
        if mem > self.high_alert:
            out = self._err_text(out)
        elif mem > self.high_warn:
            out = self._color_text(out, fg=self.cfg.memory.color_bg,
                                   bg=self.cfg.memory.color_fg)
        elif self.cfg.memory.show_always == 'True':
            out = self._color_text(out, fg=self.cfg.memory.color_fg,
                                   bg=self.cfg.memory.color_bg)
        else:
            out = ""
        return (self.__module__, self._out_format(out))
