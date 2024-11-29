# Copyright (C) 2024 Brandon Namgoong
# Written for Windows Server Datacenter scheduled task
# This web-scraping script is purely for research and documentation purposes only
# This project is not affiliated in any way by the KCNA Watch database

"""
Helper file for final result.
"""

from datetime import date
import os
import shutil

def save(day: date, loc: str, raw = False):
    """
    Save final video to media location. Will use processed broadcast by default.
    """

    dir = "{}/{}".format(loc, day.strftime("%Y %m"))
    if not os.path.exists(dir):
        os.mkdir(dir)
        if verbose: print(day.strftime("created new directory for %B"))
    if raw:
        shutil.copyfile("../downloaded/dl-%s.mp4" % day.isoformat(), "{}/Full Broadcast {}.mp4".format(dir, day.strftime("%Y %m %d")))
    else:
        shutil.copyfile("../downloaded/proc-%s.mp4" % day.isoformat(), "{}/Full Broadcast {}.mp4".format(dir, day.strftime("%Y %m %d")))

def clean():
    """
    Remove all files in 'downloaded' directory.

    Use caution when using, only call once files are not needed.
    """

    for fn in os.listdir("../downloaded"):
        file = os.path.join("../downloaded", fn)
        if os.path.isfile(file): os.remove(file)
    
    if verbose: print("working files cleaned")

# Global values
verbose: bool = False