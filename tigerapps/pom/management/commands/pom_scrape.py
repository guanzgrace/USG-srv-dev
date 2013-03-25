from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache
from pom import scrape
import os, sys
import datetime

class Command(BaseCommand):
    args = '<modules to scrape>'
    help = 'Scrapes data and stores in memcached with a timestamp'

    def handle(self, *args, **options):
        for mod_name in args:
            try:
                mod = getattr(scrape, mod_name)
            except AttributeError:
                self.stderr.write("pom.scrape.%s does not exist\n" % mod_name)
                continue
            try:
                data = mod.scrape_all()
            except:
                self.stderr.write("pom.scrape.%s failed to scrape\n" % mod_name)
                continue
            cache.set('pom.'+mod_name, (data, datetime.datetime.now()))

