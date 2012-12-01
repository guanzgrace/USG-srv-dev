from django.core.management import setup_environ
########## Essential for script
import sys,os
sys.path.insert(0,os.path.abspath("/srv/tigerapps"))
import settings
from django.core.management import setup_environ
setup_environ(settings)
###########
from django.core.mail import send_mail, BadHeaderError
from dvd.models import *
import datetime, sys

def email_if_available(dvd):
    # who to send notices to about what which dvd
    notices = Notice.objects.filter(dvd = dvd)
    for notice in notices:
        try:
            send_mail(
                dvd.name + " Now Available From USG DVDs!",
                "Hello!\nYour copy of " + dvd.name + " is now available at the USG Office!\nThanks,\nThe Princeton USG IT Commitee",
                "DO_NOT_REPLY@tigerapps.org",
                [notice.netid + "@princeton.edu"] 
            )
            return
        except BadHeaderError:
            send_mail("USG DVD email error", "Notification to " + notice.netid +  " has failed.", "DO_NOT_REPLY@tigerapps.org", ['AS1193@aol.com'], fail_silently=False)
            return

def notify_if_late():
    if True:#settings.REMINDER_EMAILS:
        now = datetime.datetime.now()
        rentalList = Rental.objects.filter(dateReturned=None).filter(dateDue__lte=now)
        
        subject = "[USG DVD] Reminder"
        from_email = "DO_NOT_REPLY@tigerapps.org"

        for rental in rentalList:
            message = "Your rental of " + rental.dvd.name + " was due on " + str(rental.dateDue) + ". Please return it as soon as you can.\nThanks,\nThe USG"
            to_email  = [rental.netid + "@princeton.edu"]
            try:
                send_mail(subject, message, from_email, ["AS1193@aol.com"], fail_silently=False)
                #send_mail(subject, message, from_email, to_email)
            except BadHeaderError:
                send_mail("USG DVD email error", "Notification to " + to_email +  " has failed.", "DO_NOT_REPLY@tigerapps.org", ['AS1193@aol.com'], fail_silently=False)
            


