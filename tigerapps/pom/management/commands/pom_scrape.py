from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from utils import cronlog
from pom.scrape import laundry, menus, printers

class Command(BaseCommand):
    args = '<modules to scrape>'
    help = 'Scrapes data and stores in memcached with a timestamp'

    def handle(self, *args, **options):
        scrape = {'laundry':laundry, 'menus':menus, 'printers':printers}
        for mod_name in args:
            try:
                mod = scrape[mod_name]
            except KeyError:
                self.stderr.write(cronlog.fmt("pom.scrape.%s does not exist" % mod_name))
                continue
            try:
                data = mod.scrape()
            except:
                self.stderr.write(cronlog.fmt("pom.scrape.%s failed to scrape/render" % mod_name))
                continue
            cache.set('pom.'+mod_name, data)
            self.stdout.write(cronlog.fmt("pom.scrape.%s scraped/rendered successfully" % mod_name))
