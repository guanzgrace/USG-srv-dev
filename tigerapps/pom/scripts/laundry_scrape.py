import sys
import datetime
from time import strftime
import memcache, requests
import pom.scrape.laundry as laundry
from pom.bldg_info import *
import cronlog

if __name__ == "__main__":
    try:
        data = laundry.scrape()
    except:
        sys.stderr.write(cronlog.fmt("pom.scrape.laundry failed to scrape/render"))
        sys.exit()
    mcdev = memcache.Client(['dev.tigerapps.org:11211'], debug=0)
    mcdev.set(':1:pom.laundry', data)
    mcprod = memcache.Client(['www.tigerapps.org:11211'], debug=0)
    mcprod.set(':1:pom.laundry', data)
    sys.stdout.write(cronlog.fmt("pom.scrape.laundry scraped/rendered successfully"))

