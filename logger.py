# Copyright (C) 2024 Brandon Namgoong
# Written for Windows Server Datacenter scheduled task
# This web-scraping script is purely for research and documentation purposes only
# This project is not affiliated in any way by the KCNA Watch database

"""
Utility for logging. Please import.
"""

from datetime import datetime

def log(message: str):
    """
    Print a message with a timestamp.
    """

    print("[{}] {}".format(datetime.now().strftime("%H:%M:%S"), message))