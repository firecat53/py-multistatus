#!/usr/bin/env python
"""This startwm.py script starts monsterwm and the statusbar. The output from
monsterwm is written to a fifo

"""
from os import mkfifo
from os.path import exists
from subprocess import Popen, PIPE

fifo = '/tmp/monsterwm.fifo'
wm = 'monsterwm'
bar = 'multistatus'

if not exists(fifo):
    mkfifo(fifo)

# Monsterwm exit code 0 for restart, 1 for quit
ret_code = 0
while not ret_code:
    bar_process = Popen(bar, stdin=PIPE, stdout=PIPE)
    mw = Popen(wm, stdout=PIPE)
    res = mw.stdout.readline()
    with open(fifo, 'w') as f:
        while res:
            f.write(res.decode())
            # This try/except catches the error if the fifo reader (statusbar)
            # is suddenly shut down to prevent the wm from crashing.
            # There will still be a high CPU usage if this happens.
            try:
                f.flush()
            except BrokenPipeError:
                continue
            res = mw.stdout.readline()
    mw.wait()
    bar_process.terminate()
    ret_code = mw.returncode
