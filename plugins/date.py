import psutil
from .worker import Worker


class PluginDate(Worker):
    """Display current date/time.

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)

    def _update_data(self):
        now = psutil.time.strftime("%a %d %b %H:%M")
        out = self._color_text(now, fg=self.cfg.date.color_fg)
        return (self.__module__, self._out_format(out))
