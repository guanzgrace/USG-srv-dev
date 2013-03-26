from django.core.management.base import BaseCommand, CommandError
from dvd import emails
from utils import cronlog

class Command(BaseCommand):
    args = ''
    help = 'Sends emails to users who have overdue DVDs'

    def handle(self, *args, **options):
        emails.notify_if_late()
        self.stdout.write(cronlog.fmt("Emails sent to users with overdue DVDs"))

