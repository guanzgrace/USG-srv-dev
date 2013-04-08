"""
Script to scrape laundry data on a Princeton server (since that site limits visitors to
Princeton IP's only), and put that data onto the tigerapps servers.
"""
import sys, datetime, traceback
from time import strftime
import memcache, requests
from pom.scrape import laundry
from pom.bldg_info import *
import cronlog

if __name__ == "__main__":
    try:
        data = laundry.scrape()
    except:
        sys.stderr.write(cronlog.fmt("pom.scrape.laundry failed to scrape/render"))
        for line in traceback.format_exc().split("\n"):
            sys.stderr.write('\t%s\n' % line)
        sys.exit()
    mcdev = memcache.Client(['dev.tigerapps.org:11211'], debug=0)
    mcdev.set(':1:pom.laundry', data)
    mcprod = memcache.Client(['www.tigerapps.org:11211'], debug=0)
    mcprod.set(':1:pom.laundry', data)
    sys.stdout.write(cronlog.fmt("pom.scrape.laundry scraped/rendered successfully"))

