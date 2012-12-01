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
            print dvd.name + " " + notice.netid
            return
        except BadHeaderError:
            send_mail("USG DVD email error", "Notification to " + notice.netid +  " has failed.", "DO_NOT_REPLY@tigerapps.org", ['AS1193@aol.com'], fail_silently=False)
            print dvd.name + " " + notice.netid
            return
