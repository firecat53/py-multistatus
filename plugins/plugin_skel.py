from .worker import Worker


class Plugin<name>(Worker):
    """New plugin

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)

    def _update_data(self):
        new = get new data (string)
        out = self._color_text(new, fg=self.cfg.<name>.color_fg, bg=self.cfg.<name>.color_bg)
        return (self.__module__, self._out_format(out))
