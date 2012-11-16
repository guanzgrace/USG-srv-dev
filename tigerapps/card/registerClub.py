########## Essential for script
import sys,os
sys.path.insert(0,os.path.abspath("/srv/tigerapps"))
import settings
from django.core.management import setup_environ
setup_environ(settings)
###########

from card.models import Member, Club

club = Club.objects.get(name=sys.argv[1])

if sys.argv[3] == "True":
    save = True
else:
    save = False

f = open(sys.argv[2])
line = f.readline()
netids = line.split(",")
for netid in netids:
    try:
        member = Member.objects.get(netid=netid)
        member.club = club
        member.is_active = True
        if save:
            member.save()
        #print member.first_name
    except:
        print netid