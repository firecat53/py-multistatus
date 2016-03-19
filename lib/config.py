from collections import namedtuple
from configparser import ConfigParser
from os.path import expanduser, join
from queue import Queue
from sys import modules

locations = ("/usr/share/py-multistatus",
             expanduser("~/.local/share/py-multistatus"),
             expanduser("~/.config/py-multistatus"))
parse = ConfigParser()
parse.read([join(i, 'status.cfg') for i in locations])

queue = Queue()

this = modules[__name__]
# (section, <items>)
for sec, item in parse.items():
    nt = namedtuple("nt", item)
    if sec != "DEFAULT":
        setattr(this, sec, nt._make(parse[sec].values()))

# Set some bar color attributes
bar = bar._replace(norm_fg=bar.fg_sym.format(bar.norm_fg))
bar = bar._replace(norm_bg=bar.bg_sym.format(bar.norm_bg))
bar = bar._replace(sel_fg=bar.fg_sym.format(bar.sel_fg))
bar = bar._replace(sel_bg=bar.bg_sym.format(bar.sel_bg))
bar = bar._replace(err_fg=bar.fg_sym.format(bar.err_fg))
bar = bar._replace(err_bg=bar.bg_sym.format(bar.err_bg))
bar = bar._replace(sep_fg=bar.fg_sym.format(bar.sep_fg))
bar = bar._replace(sep_bg=bar.bg_sym.format(bar.sep_bg))

if bar.sep_space == 'True':
    bar = bar._replace(separator=" {} ".format(bar.separator))

# Color the separator
bar = bar._replace(separator="{}{}{}{}".format(bar.sep_fg,
                                               bar.sep_bg,
                                               bar.separator,
                                               bar.reset_sym))
