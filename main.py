#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo using the new (beta) MovieStim2 to play a video file. Path of video
needs to updated to point to a video you have. MovieStim2 does /not/ require
avbin to be installed.

Movie2 does require:
1. Python OpenCV package (so openCV libs and the cv2 python interface).
    * For Windows, a binary installer is available at
        http: //www.lfd.uci.edu/~gohlke/pythonlibs/  # opencv
    * For Linux, it is available via whatever package manager you use.
    * For OSX, ..... ?
2. VLC application. The architeceture of this needs to match your psychopy/python installation 64/32 bit
    whether or not your *operating system* is 64/32 bit
    http: //www.videolan.org/vlc/index.html
"""

from __future__ import division

from psychopy import visual, core, event, parallel
import time, os
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

parallel_port = parallel.ParallelPort(address=0xD010) # TMS box address = D010?

videopath = r'./jwpIntro.mov'
videopath = os.path.join(os.getcwd(), videopath)
if not os.path.exists(videopath):
    raise RuntimeError("Video File could not be found:" + videopath)

win = visual.Window([1024, 768])

# Create your movie stim.
mov = visual.MovieStim2(win, 
                        videopath,
                        size=640,
                        # pos specifies the /center/ of the movie stim location
                        pos=[0, 0],
                        flipVert=False, flipHoriz=False,
                        loop=False)

# Start the countdown
timer_started = False

# Start the movie stim by preparing it to play
shouldflip = mov.play()
while mov.status != FINISHED:

    # Start the timer unless it has been started previously
    if not timer_started:
        timer = core.CountdownTimer(4) # in seconds
        timer_started = True
        parallel_port.setData(0) # send a zero at the start of each movie

    # Only flip when a new frame should be displayed. Can significantly reduce
    # CPU usage. This only makes sense if the movie is the only /dynamic/ stim
    # displayed.
    if shouldflip:
        # Movie has already been drawn , so just flip
        win.flip()
    else:
        # Give the OS a break if a flip is not needed
        time.sleep(0.001)
    # Draw movie stim again. Updating of movie stim frames as necessary
    # is handled internally.
    shouldflip = mov.draw()

    # Check for countdown has elapsed
    if timer.getTime() < 0:
        parallel_port.setData(1) # send a one to the TMS machine to make it send a pulse

win.close()
core.quit()
