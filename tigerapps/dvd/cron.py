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

def reminder():
    if True:#settings.REMINDER_EMAILS:
        now = datetime.datetime.now()
        rentalList = Rental.objects.filter(dateReturned=None).filter(dateDue__lte=now)
        
        subject = "[USG DVD] Reminder"
        from_email = "DO_NOT_REPLY@tigerapps.org"
        to_email = []
        print str(len(rentalList))
        print rentalList[22]
        print rentalList[24]
        print rentalList[23]
        print "================="
        for rental in rentalList:
            #message = "Your rental of " + rental.dvd.name + " was due on " + str(rental.dateDue) + ". Please return it as soon as you can.\nThanks,\nThe USG"
            #to_email.append(rental.netid + "@princeton.edu")
            print rental
            
        try:
           # send_mail(subject, message, from_email, to_email)
           print "success!"
        except BadHeaderError:
            print "failure"
            #send_mail("USG DVD email error", "Notification to " + rental.netid +  " has failed.", "DO_NOT_REPLY@tigerapps.org", ['AS1193@aol.com'], fail_silently=False)
            

def notice():
    # who to send notices to about what which dvd
    notices = Notice.objects.filter()
    check_these_users = []
    for entry in notices:
        #strings of all netids, no repeats
        check_these_users.append(str(entry.netid))
    check_these_users = list(set(check_these_users))
    #all dvds
    dvd_data = DVD.objects.filter()
    for netid in check_these_users:
        # notices for netid
        dvds_for_netid = notices.filter(netid = netid)
        dvd_strings = []
        # dvds for that netid as string
        #print netid + " WANTS: "
        for dvd in dvds_for_netid:
            dvd_strings.append(str(dvd.dvd))
            #print str(dvd.dvd)
        for check_dvd in dvd_strings:
            dvd = dvd_data.filter(name = check_dvd)
            if dvd and (dvd[0].amountLeft > 0):
                print "send mail to " + netid + check_dvd
                try:
                    send_mail(
                        check_dvd + " Now Available From USG DVDs!",
                        "Hello!\nYour copy of " + check_dvd + " is now available at the USG Office!\nThanks,\nThe Princeton USG IT Commitee",
                        "DO_NOT_REPLY@tigerapps.org",
                         ["AS1193@aol.com"]
                        #[netid + "@princeton.edu"]
                        )
                except BadHeaderError:
                    send_mail("USG DVD email error", "Notification to " + rental.netid +  " has failed.", "DO_NOT_REPLY@tigerapps.org", ['AS1193@aol.com'], fail_silently=False)
                    #print "fail"
 
if __name__ == "__main__":
    reminder()
    notice()
