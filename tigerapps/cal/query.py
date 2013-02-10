from datetime import datetime, timedelta
from django.db.models import Q
from cal.models import Event, View, RSVP
from cal.templatetags.app_extras import time_difference
from cal.globalsettings import dtdeleteflag


#####
# To fetch events
#####

def get_sded(timeselect, start_day):
    if timeselect == "upcoming":
        end_day = get_end_day_upcoming(start_day)
    elif timeselect == "day":
        end_day = start_day + timedelta(days=1)
    elif timeselect == "week":
        start_day -= timedelta(days=start_day.weekday())
        end_day = start_day + timedelta(weeks=1)
    elif timeselect == "month":
        start_day -= timedelta(days=start_day.day-1)
        yr = start_day.year + (start_day.month == 12)
        mt = start_day.month % 12 + 1
        end_day = datetime(yr, mt, 1, 0, 0, 0)
    else:
        raise Exception("Invalid argument: timeselect == %s" % timeselect)
    return start_day, end_day

def get_end_day_upcoming(sd):
    sd_z = datetime(sd.year, sd.month, sd.day, 0, 0, 0)
    return sd_z + timedelta(days=14-sd.weekday())
    
def query_upcoming():
    start_day = datetime.now()
    end_day = get_end_day_upcoming(start_day)
    return Q(event_date_time_start__gte=start_day, event_date_time_start__lte=end_day)


def events_general(start_day, end_day, query, tag_ids, feat_ids, creator, rsvp_user=0):
    events = Event.objects.filter(event_date_time_start__gte=start_day, event_date_time_start__lte=end_day)

    if query:
        q = Q()
        for word in query:
            q |= Q(event_cluster__cluster_title__icontains=word) | Q(event_cluster__cluster_description__icontains=word) | Q(event_cluster__cluster_tags__category_name__icontains=word) | Q(event_cluster__cluster_features__feature_name__icontains=word)
        events = events.filter(q)
    if tag_ids:
        tags = EventCategory.objects.filter(id__in=tag_ids)
        events = events.filter(event_cluster__cluster_tags__in=tags)
    if feat_ids:
        feats = EventFeature.objects.filter(id__in=feat_ids)
        events = events.filter(event_cluster__cluster_features__in=feats)
    if creator:
        try:
            caluser = CalUser.objects.get(user_netid=creator)
        except:
            raise Exception("Invalid argument: creator == %s" % creator)
        events = events.filter(event_cluster__cluster_user_created=caluser)

    events = events.order_by('event_date_time_start')
    
    #group the events by date
    d1 = start_day.date()
    d2 = end_day.date()
    delta = d2 - d1
    grouped_events = []
    now = datetime.today()
    for i in xrange(delta.days):
        day = d1 + timedelta(days=i)
        if day.year == now.year:
            group = day.strftime("%A, %B %e")
        else:
            group = day.strftime("%A, %B %e, %Y")
        grouped_events.append((group, []))
    for event in events:
        ind = (event.event_date_time_start.date() - d1).days
        if rsvp_user != 0:
            grouped_events[ind][1].append((event, rsvp_for_event(event,rsvp_user)))
        else:
            grouped_events[ind][1].append(event)
    return grouped_events


def events_hot(limit=0, group=True, rsvp_user=0):
    events = Event.objects.filter(event_date_time_end__gte=datetime.now(), event_attendee_count__gte=1).exclude(event_date_time_start=dtdeleteflag).order_by('-event_attendee_count')
    if limit:
        events = events[0:limit]
    if group:
        return events2grouped(events, group_hot, rsvp_user)
    return events

def events_new(limit=0, group=True, rsvp_user=0):
    events = Event.objects.filter(event_date_time_start__gte=datetime.now()).exclude(event_date_time_start=dtdeleteflag).order_by('-event_date_time_created')
    if limit:
        events = events[0:limit]
    if group:
        return events2grouped(events, group_new, rsvp_user)
    return events

def events_myviewed(user, limit=0, group=True, rsvp_user=0):
    events = []
    if not user:
        return events
    views = View.objects.filter(view_viewer=user).order_by('-view_date_time')
    if limit:
        views = views[0:limit]
    for v in views:
        v.view_event.view_date_time = v.view_date_time
        events.append(v.view_event)
    if group:
        return events2grouped(events, group_myviewed, rsvp_user)
    return events


#####
# To group or otherwise process fetched events
#####

def events2grouped(events, group_func, rsvp_user=0):
    grouped_events = []
    last_group = None
    last_list = None
    for event in events:
        group = group_func(event)
        if group != last_group:
            last_group = group
            last_list = []
            grouped_events.append((last_group, last_list))
        if rsvp_user != 0:
            last_list.append((event, rsvp_for_event(event, rsvp_user)))
        else:
            last_list.append(event)
    return grouped_events

def rsvps2grouped(rsvps, group_func):
    grouped_events = []
    last_group = None
    last_list = None
    for rsvp in rsvps:
        event = rsvp.rsvp_event
        group = group_func(event)
        if group != last_group:
            last_group = group
            last_list = []
            grouped_events.append((last_group, last_list))
        last_list.append((event, rsvp))
    return grouped_events

ATTENDEE_GROUPS = (10, 25, 50, 100)
def group_hot(event):
    i = 0
    for n in ATTENDEE_GROUPS:
        if event.event_attendee_count <= n:
            return "%d-%d Attendees" % (i, n)
        i = n
    return "100+ Attendees"

def group_new(event):
    return "Added %s ago" % time_difference(event.event_date_time_created)

def group_myviewed(event):
    return "Viewed %s ago" % time_difference(event.view_date_time)

def rsvp_for_event(event, user):
    try:
        return RSVP.objects.get(rsvp_event=event, rsvp_user=user)
    except RSVP.DoesNotExist:
        return None

#####
# To fetch RSVPs
#####

def rsvps_accepted(user, limit=0):
    rsvps = RSVP.objects.filter(rsvp_user=user, rsvp_event__event_date_time_start__gte=datetime.now(), rsvp_type='Accepted').order_by('rsvp_event__event_date_time_start')
    if limit:
        return rsvps[0:limit]
    return rsvps

def rsvps_pending(user, limit=0):
    rsvps = RSVP.objects.filter(rsvp_user=user, rsvp_event__event_date_time_start__gte=datetime.now(), rsvp_type='Pending').order_by('rsvp_event__event_date_time_start')
    if limit:
        return rsvps[0:limit]
    return rsvps


