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
from .worker import Worker
from subprocess import Popen, PIPE


class PluginMusic(Worker):
    """Displays currently playing music
    1. Mpd -- requires mpd and mpc
    2. Pianobar
    3. Mopidy

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)

    def _mpd(self):
        """Parse MPD play/pause status and music title and artist and display

        """
        cur = Popen(["mpc", "--format", "%artist%***%title%"],
                    stdout=PIPE).communicate()[0].decode().split("\n")[:-1]
        if len(cur) == 1 and 'error' in cur[0]:
            # MPD daemon not running
            return None, None
        elif len(cur) == 1:
            # MPD music stopped
            return None, None
        elif len(cur) == 3:
            # MPD playing or paused
            artist, title = cur[0].split("***")
            if self.cfg.music.show_title == 'True' and self.cfg.music.show_artist == 'True':
                display = "{} - {}".format(title, artist)
            elif self.cfg.music.show_artist == "True":
                display = artist
            elif self.cfg.music.show_title == "True":
                display = title
            play = cur[1].split()[0]
        else:
            # Unknown MPC output
            return None, None
        if play == '[playing]':
            play = self.cfg.music.play_icon
        elif play == '[paused]':
            play = self.cfg.music.pause_icon
        return play, display

    def _update_data(self):
        play, disp = self._mpd()
        if disp is None:
            out = play = ""
        elif len(disp) > int(self.cfg.music.max_width):
            # -3 : 1 for icon, 2 for ..
            out = "{}..".format(disp[:int(self.cfg.music.max_width) - 3])
        else:
            out = disp
        out = "{}{}".format(play, out)
        out = self._color_text(out, fg=self.cfg.music.color_fg,
                               bg=self.cfg.music.color_bg)
        return (self.__qualname__, self._out_format(out))
