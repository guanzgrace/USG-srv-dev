from django.http import *
from render import render_to_response
from django.contrib.auth import login
import urllib, re
from models import *
from cauth import *
from rsvp import *
from forms import *
from views_events import *
from decorators import login_required
from datetime import datetime, timedelta


@login_required
def activityFeed(request):
    user = current_user(request)
    if user.user_netid not in SITE_ADMINS:
        return HttpResponseRedirect('/')

    cutoff = datetime.now() - timedelta(hours = 48)

    feedItems = []

    userLogins = CalUser.objects.filter(user_last_login__gte=cutoff)
    for ul in userLogins:
        feedItems.append((ul.user_last_login,'%s: %s logged in' % (ul.user_last_login.strftime("%d/%m/%y %I:%M%p"),ul.full_name_suffix())))

    clusterCreated = EventCluster.objects.filter(cluster_date_time_created__gte=cutoff)
    for cc in clusterCreated:
        feedItems.append((cc.cluster_date_time_created,'%s: %s created event cluster \'%s\'' % (cc.cluster_date_time_created.strftime("%d/%m/%y %I:%M%p"),cc.cluster_user_created.full_name_suffix(), cc.cluster_title)))

    bMessages = BoardMessage.objects.filter(boardmessage_time_posted__gte = cutoff)
    for bm in bMessages:
        feedItems.append((bm.boardmessage_time_posted,'%s: %s posted a message to event cluster \'%s\'' % (bm.boardmessage_time_posted.strftime("%d/%m/%y %I:%M%p"),bm.boardmessage_poster.full_name_suffix(), bm.boardmessage_eventcluster.cluster_title)))

    rsvps = RSVP.objects.filter(rsvp_date_created__gte=cutoff)
    for rsvp in rsvps:
        if rsvp.rsvp_referrer:
            feedItems.append((rsvp.rsvp_date_created,'%s: %s has a %s RSVP to event \'%s\' from %s' % (rsvp.rsvp_date_created.strftime("%d/%m/%y %I:%M%p"),rsvp.rsvp_user.full_name_suffix(), rsvp.rsvp_type, rsvp.rsvp_event.displayname(), rsvp.rsvp_referrer.full_name_suffix())))
        else:
            feedItems.append((rsvp.rsvp_date_created,'%s: %s has a %s RSVP to event \'%s\'' % (rsvp.rsvp_date_created.strftime("%d/%m/%y %I:%M%p"),rsvp.rsvp_user.full_name_suffix(), rsvp.rsvp_type, rsvp.rsvp_event.displayname())))    

    views = View.objects.filter(view_date_time__gte=cutoff)
    for v in views:
        feedItems.append((v.view_date_time,'%s: %s viewed \'%s\' for the %s time' % (v.view_date_time.strftime("%d/%m/%y %I:%M%p"),v.view_viewer.full_name_suffix(), v.view_event.displayname(),v.view_count)))

    feedItems = sorted(feedItems, key=lambda item: item[0], reverse=True)

    dict = {}
    dict['happenings'] = feedItems

    return render_to_response(request, 'cal/easteregg.html', dict)


def userlookup(request):
    if request.method == 'GET' and 'netid' in request.GET:
        netid = request.GET.get('netid',None);
        results = gdi(netid)
        dn = results['displayName']
        return HttpResponse(dn);
    else:
        return HttpResponse('<html><body>Invalid request</body></html>');

