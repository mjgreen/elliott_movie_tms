"""
MovieStim2 does /not/ require avbin to be installed.

MovieStim2 does require:

1. Python OpenCV package (so openCV libs and the cv2 python interface).

pip install opencv-python
sudo pacman -Syu base-devel opencv opencv-samples
sudo pacman -S hdf5

2. VLC application. The architecture of this needs to match your
    psychopy/python installation 64/32 bit whether or not your
    *operating system* is 64/32 bit. http: //www.videolan.org/vlc/index.html

sudo pacman -S vlc
pip install python-vlc
"""

from __future__ import division

from psychopy import visual, core, event, parallel, monitors, gui
import time, os, sys, subprocess
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)


def pingTMS(ping_at):
    port.setData(1)  # send a one to the TMS machine to make it send a pulse
    print("\nping with {} milliseconds on the timer\n".format(round(ping_at*1000, 6)))

def pingDummy(ping_at):
    print("ping {} seconds after the timer elapsed".format(round(ping_at, 6)))
    print("ping {} milliseconds after the timer elapsed".format(round(ping_at*1000, 6)))
    print("")


# Initialise the parallel port if it exists, otherwise run the script with a dummy parallel port
if os.path.exists('/dev/parport0'):
    port = parallel.ParallelPort('/dev/parport0')
else:
    port = "dummy_port"
    print("\nWARNING: Proceeding with a dummy port\n")


videopath = r'./movies/jwpIntro.mov'
videopath = os.path.join(os.getcwd(), videopath)
if not os.path.exists(videopath):
    raise RuntimeError("Video File could not be found:" + videopath)

benq = monitors.Monitor(name="benq", width=53.5, distance=75.0)
benq.saveMon()
win = visual.Window(size=[1024, 768], pos=[(1920-1024)/2, (1080-768)/2], monitor=benq, allowGUI=False)

mov = visual.MovieStim2(win, videopath, size=640, pos=[0, 0], flipVert=False, flipHoriz=False, loop=False)

# Initialise the countdown
timer = None
timer_started = False
timer_finished = False
timer_value = 2

# Send a zero to the TMS machine.
# Sending a value to the TMS device when the countdown finishes
# will only have an effect if the value sent differs from the value
# that the port had on it immediately before -
# i.e., the trigger only has an effect if it changes the current state of the port
if port is not "dummy_port":
    port.setData(0)

# Start the movie stim by preparing it to play
shouldflip = mov.play()
while mov.status != FINISHED:

    # Start the timer unless it has been started previously.
    # The reason this is inside the loop is that there can be a delay between issuing
    # mov.play() and the first frame of the movie appearing on the screen (start-up lag)
    if not timer_started:
        timer = core.CountdownTimer(timer_value)  # in seconds
        timer_started = True

    # Check whether countdown has elapsed
    if timer.getTime() < 0.0025 and timer_finished is False:
        if port is not "dummy_port":
            ping_time = timer.getTime()
            pingTMS(ping_at=ping_time)
            timer_finished = True
        if port is "dummy_port":
            ping_time = timer.getTime()
            pingDummy(ping_at=ping_time)
            timer_finished = True

    # Check for user pressed escape
    if len(event.getKeys(keyList='escape')):
        print("user pressed escape\n")
        core.quit()

    if shouldflip:
        # Movie has already been drawn , so just flip
        win.flip()
    else:
        # Give the OS a break if a flip is not needed
        time.sleep(0.001)

    # Draw movie stim again. Updating of movie stim frames as necessary is handled internally.
    shouldflip = mov.draw()

win.close()
core.quit()
