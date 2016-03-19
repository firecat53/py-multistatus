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
