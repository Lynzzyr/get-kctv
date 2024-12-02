# Copyright (C) 2024 Brandon Namgoong
# Written for Windows Server Datacenter scheduled task
# This web-scraping script is purely for research and documentation purposes only
# This project is not affiliated in any way by the KCNA Watch database

from datetime import date
from selenium import webdriver
import argparse

import get
import marker
import result

# Process broadcast if specified
def _process(day: date):
    if args.ch:
        times: list[str] = marker.search(day)
        if not times
        if args.v: print("broadcast processed")
    else:
        if args.v: print("processing skipped")

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

    get.verbose = marker.verbose = result.verbose = args.v

    ops = webdriver.ChromeOptions()
    ops.add_argument("--headless=new")
    if not args.w:
        get.driver = webdriver.Chrome(
            options = ops
        )
    else:
        get.driver = webdriver.Chrome(
            options = ops,
            service = webdriver.ChromeService(executable_path = args.w)
        )
    
    if args.v: print("webdriver loaded")

    if args.ed:
        for day in get.get_range(args.sd, args.ed):
            get.get_broadcast(day, args.k)
            get.driver.quit()
            _process(day)
            result.save(day, args.l, args.ch)
    else:
        day: date = None
        if args.sd:
            day = date.fromisoformat(args.sd)
        else:
            day = get.get_yesterday()

        get.get_broadcast(day, args.k)
        get.driver.quit()
        _process(day)
        result.save(day, args.l, args.ch)

    result.clean()

    if args.v: print("done!")
    quit()