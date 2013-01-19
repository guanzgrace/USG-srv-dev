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
            message = "Hello!\nYour copy of " + dvd.name + " is now available at the USG Office!\nThanks,\nThe Princeton USG IT Commitee"
            to_email = [notice.netid + "@princeton.edu"]
            send_mail(
                dvd.name + " Now Available From USG DVDs!",
                message,
                "DO_NOT_REPLY@tigerapps.org",
                [notice.netid + "@princeton.edu"] 
            )

            now = datetime.datetime.now()
            f = open("/srv/tigerapps/logs/dvd_email_logs", "a")
            f.write("\n************************\n")
            f.write(str(now) + '\n')
            f.write("SENT TO: " + to_email[0])
            f.write("\nMESSAGE: \n" + message)
            f.write("\n************************\n")
            f.close()           
            return
        except BadHeaderError:
            send_mail("USG DVD email error", "Notification to " + notice.netid +  " has failed.", "DO_NOT_REPLY@tigerapps.org", ['AS1193@aol.com'], fail_silently=False)
            return

def notify_if_late():
    # Only send email if movie is due today
    now = datetime.datetime.now()
    today_begin = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0)
    today_end = datetime.datetime(now.year, now.month, now.day, 23, 59, 59, 999999)
    nov_30_12 = datetime.date(2012, 11, 30) 
    rentalList = Rental.objects.filter(dateReturned=None).filter(dateDue__lte=today_end,
                                                                     dateDue__gte=today_begin,
                                                                     dateRented__gte=nov_30_12)
    subject = "[USG DVD] Reminder"
    from_email = "DO_NOT_REPLY@tigerapps.org"
    for rental in rentalList:
        message = "Hello!\nYour rental of " + rental.dvd.name + " was due on " + str(rental.dateDue) + ". Please return it as soon as you can.\nThanks,\nThe USG"
        to_email  = [rental.netid + "@princeton.edu"]
        try:
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            now = datetime.datetime.now()
            f = open("/srv/tigerapps/logs/dvd_email_logs", "a")
            f.write("\n************************\n")
            f.write(str(now) + '\n')
            f.write("SENT TO: " + to_email[0])
            f.write("\nMESSAGE: \n" + message)
            f.write("\n************************\n")
            f.close()
        except BadHeaderError:
            send_mail("USG DVD email error", "Notification to " + to_email +  " has failed.", "DO_NOT_REPLY@tigerapps.org", ['AS1193@aol.com'], fail_silently=False)
