import psutil
from .worker import Worker


class PluginDiskUsage(Worker):
    """Display disk usage for mounted drives if over a certain threshhold.

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)

    def _update_data(self):
        out = []
        mounts = [i.mountpoint for i in psutil.disk_partitions()]
        for disk in mounts:
            try:
                use = psutil.disk_usage(disk).percent
            except PermissionError:
                continue
            if use > int(self.cfg.disk_usage.disk_use_alert):
                out.append(self._err_text("{} {}% ".format(disk, use)))
            elif use > int(self.cfg.disk_usage.disk_use_warn):
                out.append(self._sel_text("{} {}% ".format(disk, use)))
            elif self.cfg.disk_usage.disk_use_norm == 'True':
                out.append(self._color_text("{} {}% ".format(disk, use),
                                            fg=self.cfg.disk_usage.color_fg,
                                            bg=self.cfg.disk_usage.color_bg))
            else:
                out.append("")

        return (self.__module__, self._out_format("".join(out)))
