from datetime import datetime, timedelta
from collections import defaultdict
from operator import itemgetter
from django.db.models import Q
from cal.models import Event, View, RSVP, EventFeature, EventCategory
from cal.templatetags.app_extras import time_difference
from cal.globalsettings import dtdeleteflag


#####
# To fetch user-specific events
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

def count_rsvps(user, rsvp_type):
    return RSVP.objects.filter(rsvp_user=user, rsvp_event__event_date_time_start__gte=datetime.now(), rsvp_type=rsvp_type).count()

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
# To fetch events - general tab
#####

def tags_general(start_day, end_day):
    # Tags: sort by most common
    tags = Event.objects.filter(event_date_time_start__gte=start_day, event_date_time_start__lt=end_day).values_list('event_cluster__cluster_tags__category_name',flat=True)
    tag_counter = defaultdict(int)
    for tag in tags:
        tag_counter[tag] += 1
    tag_counts = sorted(tuple((tag,count) for tag,count in tag_counter.iteritems()), key=itemgetter(1), reverse=True)
    return tag_counts

def feats_general(start_day, end_day):
    feats = Event.objects.filter(event_date_time_start__gte=start_day, event_date_time_start__lt=end_day).values_list('event_cluster__cluster_features__id',flat=True)
    feat_counter = defaultdict(int)
    for feat in feats:
        if feat:
            feat_counter[feat] += 1
    feat_counts = tuple((EventFeature.objects.get(id=id),count) for id,count in feat_counter.iteritems())
    return feat_counts


def get_sded(timeselect, start_day):
    if timeselect == "upcoming":
        end_day = get_end_day_upcoming(start_day)
        ts_ind = 0
    elif timeselect == "day":
        end_day = start_day + timedelta(days=1)
        ts_ind = 1
    elif timeselect == "week":
        start_day -= timedelta(days=start_day.weekday())
        end_day = start_day + timedelta(weeks=1)
        ts_ind = 2
    elif timeselect == "month":
        start_day -= timedelta(days=start_day.day-1)
        yr = start_day.year + (start_day.month == 12)
        mt = start_day.month % 12 + 1
        end_day = datetime(yr, mt, 1, 0, 0, 0)
        ts_ind = 3
    else:
        raise Exception("Invalid argument: timeselect == %s" % timeselect)
    return ts_ind, start_day, end_day

def get_end_day_upcoming(sd):
    sd_z = datetime(sd.year, sd.month, sd.day, 0, 0, 0)
    return sd_z + timedelta(days=14-sd.weekday())
    
def query_upcoming():
    start_day = datetime.now()
    end_day = get_end_day_upcoming(start_day)
    return Q(event_date_time_start__gte=start_day, event_date_time_start__lte=end_day)


DAY_GROUPS = (
    ("Early Morning (before 9:00 am)", 9, 0),
    ("Morning (9:00 am - 12:30 pm)", 12, 30),
    ("Afternoon (12:30 pm - 4:30 pm)", 16, 30),
    ("Evening (4:30 pm - 7:30 pm)", 19, 30),
    ("Night (after 7:30 pm)", 24, 0),
)

def events_general(start_day, end_day, query=None, tags=None, feats=None, creator=None, rsvp_user=0):
    events = Event.objects.filter(event_date_time_start__gte=start_day, event_date_time_start__lt=end_day)

    if query:
        q = Q()
        for word in query:
            q |= Q(event_cluster__cluster_title__icontains=word) | Q(event_cluster__cluster_description__icontains=word) | Q(event_cluster__cluster_tags__category_name__icontains=word) | Q(event_cluster__cluster_features__feature_name__icontains=word)
        events = events.filter(q)
    if tags:
        events = events.filter(event_cluster__cluster_tags__in=tags)
    if feats:
        events = events.filter(event_cluster__cluster_features__in=feats)
    if creator:
        events = events.filter(event_cluster__cluster_user_created=creator)

    events = events.order_by('event_date_time_start')
    
    #group the events by date
    d1 = start_day.date()
    d2 = end_day.date()
    delta = (d2 - d1).days
    grouped_events = []
    if delta == 1: #day timeselect
        grouped_events = tuple((day_group[0], []) for day_group in DAY_GROUPS)
        for event in events:
            h1 = event.event_date_time_start.hour
            m1 = event.event_date_time_start.minute
            for i, (group, h, m) in enumerate(DAY_GROUPS):
                if h1 < h or (h1 == h and m1 < m):
                    ind = i
                    break
            if rsvp_user != 0:
                grouped_events[ind][1].append((event, rsvp_for_event(event,rsvp_user)))
            else:
                grouped_events[ind][1].append(event)
    else: #other timeselects
        this_year = datetime.today().year
        for i in xrange(delta):
            day = d1 + timedelta(days=i)
            if day.year == this_year:
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


#####
# To fetch events - special tabs
#####

def events_hot(limit=0, group=True, rsvp_user=0):
    events = Event.objects.filter(event_date_time_end__gte=datetime.now(), event_attendee_count__gte=1).exclude(event_date_time_start=dtdeleteflag).order_by('-event_attendee_count', 'event_date_time_start')
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

