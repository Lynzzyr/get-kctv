# Copyright (C) 2024 Brandon Namgoong
# Written for Windows Server Datacenter scheduled task
# This web-scraping script is purely for research and documentation purposes only
# This project is not affiliated in any way by the KCNA Watch database

from datetime import date
from selenium import webdriver
import argparse
import asyncio

import get
import marker
import result

# Wrapper for get_broadcast
async def _get(day: date, rm: bool):
    try: get.get_broadcast(day, rm)
    except get.NullBroadcastException: return

# Main trial process
async def _attempt(day: date, rm: bool):
    for i in range(3):
        try:
            if args.verbose: print("starting timer")
            await asyncio.wait_for(_get(day, rm), timeout = 900)
            break
        except asyncio.TimeoutError:
            if args.verbose: print("timed out, restarting... (%s/3)" % i + 1)

# Process broadcast if specified
def _process(day: date):
    # if args.ch:
    #     times: list[str] = marker.search(day)
    #     if not times
    #     if args.v: print("broadcast processed")
    # else:
    #     if args.v: print("processing skipped")
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Script for fetching broadcasts of Korean Central Television from the KCNA Watch database. Will fetch broadcast of yesterday by default if -sd is not set."
    )
    parser.add_argument("-w", "--webdriver", type = str, help = "Location of Chrome webdriver binary, will use Selenium Manager to fetch webdriver if not specified")
    parser.add_argument("-sd", "--start_date", type = str, help = "Start date of range in ISO 8601 YYYY-MM-DD, -y will be ignored; use exclusively for getting only one day")
    parser.add_argument("-ed", "--end_date", type = str, help = "End date of range in ISO 8601 YYYY-MM-DD, -y will be ignored")
    parser.add_argument("-l", "--location", type = str, help = "Location of main 'Korean Central Television' show directory", required = True)
    parser.add_argument("-ch", "--chapters", action = "store_false", help = "Whether to add chapter marks corresponding to start points of each program, default True")
    parser.add_argument("-rm", "--remove_existing", action = "store_false", help = "Whether to remove existing broadcast files, default True")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "Whether to print verbose messages, default False")

    args = parser.parse_args()

    get.verbose = marker.verbose = result.verbose = args.verbose

    ops_args: list[str] = [
        "--headless=new",
        "disable-infobars",
        "--disable-extensions",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--no-sandbox"
    ]

    ops = webdriver.ChromeOptions()
    for arg in ops_args: ops.add_argument(arg)
    if not args.webdriver:
        get.driver = webdriver.Chrome(
            options = ops
        )
    else:
        get.driver = webdriver.Chrome(
            options = ops,
            service = webdriver.ChromeService(executable_path = args.webdriver)
        )
    
    if args.verbose: print("webdriver loaded")

    if args.end_date:
        for day in get.get_range(args.start_date, args.end_date):
            if args.verbose: print("PROCESS: BULK from {} to {} | on {}".format(args.start_date, args.end_date, day.isoformat()))
            asyncio.run(_attempt(day, args.remove_existing))
            _process(day)
            result.save(day, args.location)
        get.driver.quit()
    else:
        day: date = None
        if args.start_date:
            day = date.fromisoformat(args.start_date)
            if args.verbose: print("PROCESS: SINGLE on %s" % args.start_date)
        else:
            day = get.get_yesterday()
            if args.verbose: print("PROCESS: SINGLE on yesterday")

        asyncio.run(_attempt(day, args.remove_existing))
        get.driver.quit()
        _process(day)
        result.save(day, args.location)

    result.clean()

    if args.verbose: print("done!")
    quit()