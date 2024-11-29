# Copyright (C) 2024 Brandon Namgoong
# Written for Windows Server Datacenter scheduled task
# This web-scraping script is purely for research and documentation purposes only
# This project is not affiliated in any way by the KCNA Watch database

from datetime import date
from selenium import webdriver
import argparse

import get
import result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Script for fetching broadcasts of Korean Central Television from the KCNA Watch database. Will fetch broadcast of yesterday by default if -sd is not set."
    )
    parser.add_argument("-w", "--webdriver", type = str, help = "Location of Chrome webdriver binary, will use Selenium Manager to fetch webdriver if not specified")
    parser.add_argument("-sd", "--start_date", type = str, help = "Start date of range in ISO 8601 YYYY-MM-DD, -y will be ignored; use exclusively for getting only one day")
    parser.add_argument("-ed", "--end_date", type = str, help = "End date of range in ISO 8601 YYYY-MM-DD, -y will be ignored")
    parser.add_argument("-l", "--location", type = str, help = "Location of main 'Korean Central Television' show directory", required = True)
    parser.add_argument("-k", "--keep_existing", action = "store_true", help = "Whether to keep existing broadcast files, defaults to False")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "Whether to print verbose messages, default False")

    args = parser.parse_args()

    get.verbose = result.verbose = args.v
    range: bool = bool(args.ed)

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

    if range:
        for day in get.get_range(args.sd, args.ed):
            get.get_broadcast(day, args.k)
    else:
        if args.sd:
            get.get_broadcast(date.fromisoformat(args.sd), args.k)
        else:
            get.get_broadcast(get.get_yesterday(), args.k)
    
    get.driver.quit()

    # TODO add processing

    if range:
        for day in get.get_range(args.sd, args.ed):
            result.save(day, args.l)
    else:
        if args.sd:
            result.save(day.fromisoformat(args.sd), args.l)
        else:
            result.save(get.get_yesterday(), args.l)

    quit()