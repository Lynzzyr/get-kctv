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
import pathlib

# def save(day: date, loc: str, encoded: bool = True):
def save(day: date, loc: str):
    """
    Save final video to media location. Will use processed broadcast by default.
    """

    # f: str = ""
    # if encoded:
    #     f = "../temp/{}-%s.mp4".format("enc")
    # else:
    #     f = "../temp/{}-%s.mp4".format("dl")

    f: pathlib.Path = pathlib.Path("temp/dl-%s.mp4" % day.isoformat())

    dir: pathlib.Path = pathlib.Path("{}/{}".format(loc, day.strftime("%Y %m")))

    if not dir.exists():
        os.mkdir(dir)
        if verbose: print(day.strftime("created new directory for %B"))

    if verbose: print("started upload to destination...")
    shutil.copyfile(f, pathlib.Path("{}/Broadcast {}.mp4".format(dir, day.strftime("%Y %m %d"))))
    if verbose: print("saved full broadcast to %s" % dir)

def clean():
    """
    Remove all files in 'temp' directory.

    Use caution when using, only call once files are not needed.
    """

    temp: pathlib.Path = pathlib.path("temp")

    for fn in os.listdir(temp):
        file = temp / fn
        if os.path.isfile(file): os.remove(file)
    
    if verbose: print("working files cleaned")

# Global values
verbose: bool = False