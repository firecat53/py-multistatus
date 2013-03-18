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
from os.path import expanduser
from subprocess import Popen, PIPE


class PluginMusic(Worker):
    """Displays currently playing music
    1. Mpd -- requires mpd and mpc
    2. Pianobar
    3. Mopidy

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)
        self.players = self.cfg.music.players.split()
        self.display_fields = self.cfg.music.display.split()
        if self.cfg.music.pianobar_status_file:
            self.piano_status = expanduser(self.cfg.music.pianobar_status_file)

    def _mpd(self):
        """Parse MPD play/pause status and music title and artist and display

        """
        cur = Popen(["mpc", "--format", "%artist%***%title%***%album%"],
                    stdout=PIPE).communicate()[0].decode().split("\n")[:-1]
        if len(cur) == 1 and 'error' in cur[0]:
            # MPD daemon not running
            return None, None
        elif len(cur) == 1:
            # MPD music stopped
            return None, None
        elif len(cur) == 3:
            # MPD playing or paused
            artist, title, album = cur[0].split("***")
            display = ""
            display_dict = {"title": title,
                            "artist": artist,
                            "album": album}
            for field in self.display_fields:
                display = "{}{} - ".format(display, display_dict[field])
            display = display.strip(" - ")
            play = cur[1].split()[0]
        else:
            # Unknown MPC output
            return None, None
        if play == '[playing]':
            play = self.cfg.music.play_icon
        elif play == '[paused]':
            play = self.cfg.music.pause_icon
        return play, display

    def _pianobar(self):
        with open(self.piano_status) as fn:
            stat = fn.readlines()
        stat = {i.split("=", 1)[0]: i.split("=", 1)[1].strip()
                for i in stat}
        display = ""
        for field in self.display_fields:
            display = "{}{} - ".format(display, stat[field])
        display = display.strip(" - ")
        return self.cfg.music.play_icon, display

    def _mopidy(self):
        pass

    def _choose_player(self):
        """Determine which music play is currently running. This assumes that
        mpd is running all the time, so it should be last in the list

        """
        for player in self.players:
            if Popen(["pgrep", player], stdout=PIPE).communicate()[0]:
                return getattr(self, "_{}".format(player))()

    def _update_data(self):
        play, disp = self._choose_player()
        if disp is None:
            out = play = ""
        elif len(disp) > int(self.cfg.music.max_width):
            # -3 : 1 for icon, 2 for ..
            out = "{}..".format(disp[:int(self.cfg.music.max_width) - 4])
        else:
            out = disp
        if out or play:
            out = "{} {}".format(play, out)
        out = self._color_text(out, fg=self.cfg.music.color_fg,
                               bg=self.cfg.music.color_bg)
        return (self.__qualname__, self._out_format(out))
