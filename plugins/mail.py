import psutil
from collections import OrderedDict
from .worker import Worker


class PluginMailAndWeather(Worker):
    """Display current temp. If there is new mail, replace the temperature with
    new mail icons.

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)
        self.accounts = self.cfg.mail.accounts.split()

    def _count_mail(self):
        new = OrderedDict()
        for acct in self.accounts:
            new[acct] = len(psutil.os.listdir(
                             psutil.os.path.expanduser(
                                 self.cfg.mail.mail_dir_path.format(
                                     account=acct))))
        return new

    def _update_data(self):
        mail = self._count_mail()
        if sum(mail.values()) > 0:
            vals = [str(i) for i in mail.values()]
            counts = ":".join(vals)
            out = self._color_text(" {} {}".format(self.cfg.mail.icon, counts),
                                   fg=self.cfg.mail.color_bg,
                                   bg=self.cfg.mail.color_fg)
        else:
            with open(psutil.os.path.expanduser(self.cfg.mail.weather)) as f:
                out = self._color_text(f.readlines()[0].strip(),
                                       fg=self.cfg.mail.color_fg)
        return (self.__module__, self._out_format(out))
