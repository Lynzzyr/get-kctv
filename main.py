# Copyright (C) 2024 Brandon Namgoong
# Written for Windows Server Datacenter scheduled task
# This web-scraping script is purely for research and documentation purposes only
# This project is not affiliated in any way by the KCNA Watch database

from datetime import date
from selenium import webdriver
import argparse
import asyncio

import logger

import get

# Main process
async def _get(day: date, loc: str, rm: bool):
    for i in range(3):
        try:
            try: await asyncio.wait_for(get.get_broadcast(day, loc, rm), timeout = 1200) # 20 minute timeout, single download avg 10 minutes
            except get.NullBroadcastException: pass
            break
        except asyncio.TimeoutError:
            if args.verbose: logger.log("timed out, restarting... (%s/3)" % str(i + 1))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Script for fetching broadcasts of Korean Central Television from the KCNA Watch database. Will fetch broadcast of yesterday by default if -sd is not set."
    )
    parser.add_argument("-w", "--webdriver", type = str, help = "Location of Chrome webdriver binary, will use Selenium Manager to fetch webdriver if not specified")
    parser.add_argument("-sd", "--start_date", type = str, help = "Start date of range in ISO 8601 YYYY-MM-DD, -y will be ignored; use exclusively for getting only one day")
    parser.add_argument("-ed", "--end_date", type = str, help = "End date of range in ISO 8601 YYYY-MM-DD, -y will be ignored")
    parser.add_argument("-l", "--location", type = str, help = "Location of main 'Korean Central Television' show directory", required = True)
    parser.add_argument("-rm", "--remove_existing", action = "store_false", help = "Whether to remove existing broadcast files, default True")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "Whether to print verbose messages, default False")

    args = parser.parse_args()

    get.verbose = args.verbose

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
    
    if args.verbose: logger.log("webdriver loaded")

    if args.end_date:
        for day in get.get_range(args.start_date, args.end_date):
            if args.verbose: logger.log("PROCESS: BULK from {} to {} | on {}".format(args.start_date, args.end_date, day.isoformat()))
            asyncio.run(_get(day, args.location, args.remove_existing))
        get.driver.quit()
    else:
        day: date = None
        if args.start_date:
            day = date.fromisoformat(args.start_date)
            if args.verbose: logger.log("PROCESS: SINGLE on %s" % args.start_date)
        else:
            day = get.get_yesterday()
            if args.verbose: logger.log("PROCESS: SINGLE on yesterday")

        asyncio.run(_get(day, args.location, args.remove_existing))
        get.driver.quit()

    if args.verbose: logger.log("done!")
    quit()