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
from threading import Thread


class Worker(Thread):
    """Worker thread skeleton class.

    """
    def __init__(self, cfg, interval, **kwargs):
        Thread.__init__(self)
        self.cfg = cfg
        self.interval = int(interval)
        self.daemon = True

    def _update_queue(self):
        self.cfg.queue.put(self.data)

    def _sel_text(self, text):
        # Wrap string with selection color, and reset to normal fg color at the end
        return "{}{}{}{}".format(self.cfg.bar.sel_fg, self.cfg.bar.sel_bg,
                                 text, self.cfg.bar.reset_sym)

    def _err_text(self, text):
        # Wrap string with error color, and reset to normal fg color at the end
        return "{}{}{}{}".format(self.cfg.bar.err_fg, self.cfg.bar.err_bg,
                                 text, self.cfg.bar.reset_sym)

    def _color_text(self, text, fg=None, bg=None):
        if fg is None:
            fg = self.cfg.bar.norm_fg
        if bg is None:
            bg = self.cfg.bar.norm_bg
        # Wrap text in arbitrary fg/bg colors. Defaults to norm fg, norm bg. Resets
        # to norm fg, norm bg. Pass the color name as a string, "red"
        if fg != self.cfg.bar.norm_fg:
            fg = "{}{}".format(self.cfg.bar.fg_sym, getattr(self.cfg.bar, fg))
        if bg != self.cfg.bar.norm_bg:
            bg = "{}{}".format(self.cfg.bar.bg_sym, getattr(self.cfg.bar, bg))
        return "{}{}{}{}".format(fg, bg, text, self.cfg.bar.reset_sym)

    def _out_format(self, text):
        """Add the separator to the output text.

        """
        if not text:
            return ""
        else:
            return "{}{}".format(self.cfg.bar.separator, text)


    def run(self):
        while True:
            self.data = self._update_data()
            self._update_queue()
            psutil.time.sleep(self.interval)
