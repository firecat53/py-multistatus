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
import psutil
from .worker import Worker


class PluginMailAndWeather(Worker):
    """Display current temp. If there is new mail, replace the temperature with
    new mail icons.

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)
        self.accounts = self.cfg.mail.accounts.split()

    def _count_mail(self):
        new = {}
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
        return (self.__qualname__, self._out_format(out))
