from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings
import os, sys

class Command(BaseCommand):
    args = ''
    help = 'Update the html cache of the Django template toolbar'

    def handle(self, *args, **options):
        fname = os.path.join(settings.CURRENT_DIR, 'templates', 'main', '_autogen.html')
        f = open(fname, 'w')
        f.write(render_to_string('main/jquery.html'))
        f.close()

