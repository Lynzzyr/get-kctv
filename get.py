# Copyright (C) 2024 Brandon Namgoong
# Written for Windows Server Datacenter scheduled task
# This web-scraping script is purely for research and documentation purposes only
# This project is not affiliated in any way by the KCNA Watch database

"""
General webscraper for searching, accessing, and downloading broadcast archives of Korean Central Television from the KCNA Watch database.
"""

from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import aiohttp
import pathlib

import logger

# If there is no full broadcast available
class NullBroadcastException(Exception):
    def __init__(self, message = None):
        super().__init__(message)

def get_yesterday() -> date:
    """
    Get day before
    """

    return date.fromtimestamp(int(time.time()) - 86400)

def get_range(start: str, end: str) -> list[date]:
    """
    Get range of days from two ISO 8601 days
    """

    sd = date.fromisoformat(start)
    ed = date.fromisoformat(end) + timedelta(1)
    return [ sd + timedelta(d) for d in range(int((ed - sd).days)) ]

async def get_broadcast(day: date, loc: str, rm: bool = True) -> None:
    """
    Common method to webscrape and download broadcast. Saves download to specified directory.
    """

    if verbose: logger.log("starting download for: " + day.isoformat())

    url_1: str = "https://kcnawatch.org/kctv-archive/?start={date}&end={date}".format(date = day.strftime("%d-%m-%Y"))
    if verbose: logger.log("search url: %s" % url_1)
    driver.get(url_1)

    url_2: str = ""
    ars: list = driver.find_elements(By.CLASS_NAME, "article-desc")
    for op in ars:
        if ( op.find_element(By.CLASS_NAME, "broadcast-head").text != "Full Broadcast" ): continue
        url_2 = op.find_element(By.LINK_TEXT, day.strftime("%A %B %d, %Y")).get_attribute("href")
    if not url_2:
        if verbose: logger.log(day.strftime("broadcast of %B %d, %Y does not exist! quiting process"))
        raise NullBroadcastException
    if verbose: logger.log("article at: %s" % url_2)
    driver.get(url_2)

    src: str = driver.find_element(By.XPATH, "//video[@id = 'bitmovinplayer-video-player']").find_element(By.XPATH, "source").get_attribute("src")
    if verbose: logger.log("stream at: %s" % src)

    dir: pathlib.Path = pathlib.Path("{}/{}".format(loc, day.strftime("%Y %m")))
    if not dir.exists():
        os.mkdir(dir)
        if verbose: logger.log("created new month directory")
    file: pathlib.Path = dir / day.strftime("Broadcast %Y %m %d.mp4")
    if file.exists() and rm:
        os.remove(file)
        if verbose: logger.log("removed existing file")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(src) as res:
                res.raise_for_status()
                with open(file, "wb") as f:
                    if verbose: logger.log("writing to %s..." % loc)
                    async for chunk in res.content.iter_chunked(4194304):
                        f.write(chunk)
        if verbose: logger.log("fetched: %s" % day.isoformat())
    except aiohttp.ClientResponseError:
        if verbose: logger.log("stream returned null")

# Global values
driver: webdriver.Chrome = None
verbose: bool = False