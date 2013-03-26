from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from utils import cronlog
from cal.models import CalUser
from cal.calmailer import email_today_reminder
import datetime


class Command(BaseCommand):
    args = ''
    help = 'Sends reminder emails for events'

    def handle(self, *args, **options):
        self.stdout.write("------------------------------\n")
        try:
            today = datetime.date.today()
            reminderUsers = CalUser.objects.filter(user_reminders_requested = True)
            count = 0
            for user in reminderUsers:
                if email_today_reminder(user, today):
                    count += 1
            self.stdout.write(cronlog.fmt("Reminder emails sent successfully to %d users" % count))
        except Exception, e:
            self.stderr.write(cronlog.fmt("ERROR: %s" % str(e)))
        self.stdout.write("------------------------------\n")
