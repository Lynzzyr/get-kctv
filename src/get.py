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
import requests
import pathlib

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

def get_broadcast(day: date, rm: bool = True) -> None:
    """
    Common method to webscrape and download broadcast. Saves download to a directory named 'temp'.

    Will save download as 'dl-YYYY-MM-DD.mp4'.
    """

    if verbose: print("starting download for: " + day.isoformat())

    url_1: str = "https://kcnawatch.org/kctv-archive/?start={date}&end={date}".format(date = day.strftime("%d-%m-%Y"))
    if verbose: print("search url: %s" % url_1)
    driver.get(url_1)

    url_2: str = ""
    ars: list = driver.find_elements(By.CLASS_NAME, "article-desc")
    for op in ars:
        if ( op.find_element(By.CLASS_NAME, "broadcast-head").text != "Full Broadcast" ): continue
        url_2 = op.find_element(By.LINK_TEXT, day.strftime("%A %B %d, %Y")).get_attribute("href")
    if not url_2:
        if verbose: print(day.strftime("broadcast of %B %d, %Y does not exist! quiting process"))
        driver.quit()
        quit()
    if verbose: print("article at: %s" % url_2)
    driver.get(url_2)

    src: str = driver.find_element(By.XPATH, "//video[@id = 'bitmovinplayer-video-player']").find_element(By.XPATH, "source").get_attribute("src")
    if verbose: print("stream at: %s" % src)

    dir: pathlib.Path = pathlib.Path("../temp")
    if not dir.exists():
        os.mkdir(dir)
        if verbose: print("created temp directory")
    file: pathlib.Path = dir / ("dl-%s.mp4" % day.isoformat())
    try:
        with requests.get(src, stream = True) as res:
            res.raise_for_status()
            if file.exists() and rm:
                os.remove(file)
                if verbose: print("removed existing file")
            with open(file, "wb") as f:
                if verbose: print("writing...")
                for chunk in res.iter_content(chunk_size = 1048576):
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        if verbose: print(e)
    
    if verbose: print("fetched: %s" % day.isoformat())

# Global values
driver: webdriver.Chrome = None
verbose: bool = False