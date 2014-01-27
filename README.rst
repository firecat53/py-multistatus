py_multistatus
==============

Statusbar information script with configurable update intervals for each block of information. Designed for window managers using a separate bar such as LemonBoy's `bar <https://github.com/LemonBoy/bar>`_, Moetune's `some_sorta_bar <https://github.com/moetunes/Some_sorta_bar>`_ (TODO), or `dzen <https://github.com/robm/dzen>`_ (TODO). Information is generated and piped to the bar input. A configuration file is included, and plugins can easily be added if desired. Plugins (so far) include:

* Monsterwm desktop status display
* Date/time
* Load average
* New mail notifier for maildir(s) + weather display
* Disk usage warnings
* Battery status display
* Network up/down state and upload/download speed + OpenVPN status
* Music player status: MPD/Mopidy and Pianobar

Idea and code based heavily on `py3status <https://github.com/kaszak/py3status>`_. Much thanks to kaskak, as I studied his code intensely before I started. I had no prior experience with threading/queue/fifo before starting this project!

Scott Hansen <firecat4153@gmail.com>

Features:
---------

* Python 3.x
* Use less CPU cycles for infrequently needed information updates
* Configurable for different statusbars (bar, some_sorta_bar, etc.)
* Easily add new plugins (see plugin_skel.py in the plugins directory).
* Includes a python monsterstart.py script to start monsterwm and pipe its desktop output to a FIFO for reading by py-multistatus.

Requires: 
---------

* Python 3+
* psutil
* An installed statusbar (bar, some_sorta_bar, etc.)

Installation:
-------------

* `Archlinux AUR <link here>`_ (TODO)
* ``# python setup.py install``  OR
* ``$ python setup.py install --user`` OR
* ``pip install py_multistatus`` (TODO)

License:
--------

* GPL v3+

Usage:
------

* Copy configuration file status.cfg from /usr/share/py-multistatus to ~/.config/py-multistatus and edit. Make sure the bar executable and all the formatting symbols are correct for the bar you are using.
* Note: If using 'bar', it seems that the fallback font width should be set the same size as the fonts for font-icons to work right, like::

    #define BAR_FONT "-*-stlarch-medium-r-normal-*-16-*-*-*-c-*-iso10646-1", \
                     "-*-terminus-medium-r-normal-*-16-*-*-*-c-*-iso10646-1"
    /* Some fonts don't set the right width for some chars, pheex it */
    #define BAR_FONT_FALLBACK_WIDTH 16

* Ensure mail accounts and directories are correct. If you want the weather displayed while there are no mail notifications, create a text file ~/.weather with the weather add there however you like. The *top line* of the file will be displayed.
* Add ``multistatus &`` to ~/.xinitrc before the ``exec <windowmanager`` line (or before ``/path/to/monsterstart.py``)
* The bar is automatically started by ``multistatus``
* If using monsterstart.py, copy it someplace into your $PATH. It starts ``multistatus`` so use it in .xinitrc instead.

ISSUES:
-------

* Some stlarch font icons (higher numbers) cause problems with the display with 'bar'
* Network speed indicator occasionally crashes when switching networks.
* If the statusbar is killed and restarted manually, the monsterwm desktop info doesn't always immediately appear.

TODO:
-----

1. Test/add support for other bars beside LemonBoy's bar.
2. Add logging/error detection for threads. Possibly auto-restart crashed threads
3. Add option to periodically update the weather? (clickable bars only)
4. Volume indication. Maybe volume controls? (clickable bars only)
5. Possible inotify support for file-based information?
6. Investigate using concurrent.futures in place of threads/queues.
