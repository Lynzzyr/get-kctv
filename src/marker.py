# Copyright (C) 2024 Brandon Namgoong
# Written for Windows Server Datacenter scheduled task
# This web-scraping script is purely for research and documentation purposes only
# This project is not affiliated in any way by the KCNA Watch database

"""
Adds chapter marks to KCTV broadcasts at the start of every program. Requires 'ffmpeg' and 'tesseract' to be installed on host.

Attempts to use OCR to scan timestamps during the "Today's Schedule" (오늘의 순서) feature.
"""

from PIL import Image
import ffmpeg
import pytesseract

def set_bounds(start: str, stop: str):
    """
    Manually specify start and end times of 'Today's Schedule', bypassing the automatic feature checker
    """

    ss = start
    to = stop
    set = True



# Global values
ss: str = "5:00" # 5 minutes
to: str = None
set: bool = False
box: tuple[int] = (80, 100, 230, 160)
verbose: bool = False

"""
check frame every 1 second, 
"""