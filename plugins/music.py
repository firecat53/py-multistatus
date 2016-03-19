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

    def _mpd(self, port=None):
        """Parse MPD play/pause status and music title and artist and display

        """
        port = port or self.cfg.music.mpd_port
        cur = Popen(["mpc", "--port", str(port),
                     "--format", "%artist%***%title%***%album%"],
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
        return self._mpd(self.cfg.music.mopidy_port)

    def _choose_player(self):
        """Determine which music play is currently running. This assumes that
        mpd is running all the time, so it should be last in the list

        """
        for player in self.players:
            if Popen(["pgrep", player], stdout=PIPE).communicate()[0]:
                return getattr(self, "_{}".format(player))()

    def _update_data(self):
        try:
            play, disp = self._choose_player()
        except TypeError:
            play = disp = ""
        if disp and len(disp) > int(self.cfg.music.max_width):
            # -3 : 1 for icon, 2 for ..
            out = "{}..".format(disp[:int(self.cfg.music.max_width) - 4])
        else:
            out = disp
        if out or play:
            out = "{} {}".format(play, out)
        out = self._color_text(out, fg=self.cfg.music.color_fg,
                               bg=self.cfg.music.color_bg)
        return (self.__module__, self._out_format(out))
