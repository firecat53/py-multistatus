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
        # Wrap string with selection color, and reset to normal fg color at the
        # end
        if not text:
            return ""
        return "{}{}{}{}".format(self.cfg.bar.sel_fg, self.cfg.bar.sel_bg,
                                 text, self.cfg.bar.reset_sym)

    def _err_text(self, text):
        # Wrap string with error color, and reset to normal fg color at the end
        if not text:
            return ""
        return "{}{}{}{}".format(self.cfg.bar.err_fg, self.cfg.bar.err_bg,
                                 text, self.cfg.bar.reset_sym)

    def _color_text(self, text, fg=None, bg=None):
        if not text:
            return ""
        fg = fg or self.cfg.bar.norm_fg
        bg = bg or self.cfg.bar.norm_bg
        # Wrap text in arbitrary fg/bg colors. Defaults to norm fg, norm bg.
        # Resets to norm fg, norm bg.
        if fg != self.cfg.bar.norm_fg:
            fg = self.cfg.bar.fg_sym.format(fg)
        if bg != self.cfg.bar.norm_bg:
            bg = self.cfg.bar.bg_sym.format(bg)
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
