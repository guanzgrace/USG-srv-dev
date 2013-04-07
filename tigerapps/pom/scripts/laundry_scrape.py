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
    mc = memcache.Client(['174.143.241.115:11211'], debug=0)
    mc.set('pom.laundry', data)
    sys.stdout.write(cronlog.fmt("pom.scrape.laundry scraped/rendered successfully"))

