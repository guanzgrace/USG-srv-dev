################################################################
# Project: Princeton Events Calendar
# Authors: Ethan Goldstein, Samantha Hantman, Dana Hoffman, 
#           Adriana Susnea, and Michael Yaroshefsky 
# Date:    May 11, 2010
################################################################
# Title:  views_events.py
# Info :  rendering pages and executing actions related to events
################################################################

from django.core.mail import send_mail
from django.forms.formsets import formset_factory
from django.utils.encoding import smart_unicode, smart_str
from django.template import Context, loader
from django.db.models import Q, Count
from django.http import *
from django.contrib.auth import login

import urllib, re, json
from collections import defaultdict
from operator import itemgetter
from datetime import datetime, timedelta
import vobject
import cgi

from groups.models import *
from groups.email_msg import FEED_NOTIFICATION_EMAIL
from groups.globalsettings import SITE_EMAIL,EMAIL_HEADER_PREFIX
from cal.globalsettings import our_site, our_email

from utils.dsml import *
from cal.decorators import login_required
from cal.render import render_to_response
from cal.models import *
from cal.cauth import *
from cal.rsvp import *
from cal.forms import *
from cal.mailer import *
from cal.usermsg import MsgMgr
from cal import query
from cal import cal_util


def evlist_gen(request):
    out_dict = evlist_gen_inner(request, True)
    return evlist_render_page(request, out_dict)

def evlist_gen_ajax(request):
    out_dict = evlist_gen_inner(request, 'changedDates' in request.GET)
    out_json = json.dumps(out_dict)
    return HttpResponse(out_json, content_type="application/json")

def evlist_gen_inner(request, loadEvfilter):
    """
    Generate HTML of events list matching the filters in `request`
    """
    time_params, title, dates, start_day, end_day = evlist_parse_time_params(request)
    filter_params, query_words, tags, feat_ids, creator = evlist_parse_filter_params(request)

    user = current_user(request)
    grouped_events = query.events_general(start_day, end_day, query_words, tags, feat_ids, creator, user)
    inner_html = render_to_string("cal/evlist_inner.html", {'grouped_events': grouped_events})

    if loadEvfilter:
        filter_params['tagsHtml'] = render_to_string(
            "cal/modules/evfilter_tags.html",
            {'evfilter_tags': query.tags_general(start_day, end_day)})
        filter_params['featsHtml'] = render_to_string(
            "cal/modules/evfilter_feats.html",
            {'evfilter_feats': query.feats_general(start_day, end_day)})

    out_dict = {
        'evlist_inner': inner_html,
        'evlist_title': title,
        'evlist_dates': dates,
        'evlist_time_dict': time_params,
        'evlist_filter_dict': filter_params,
    }

    return out_dict


SPE_LIMIT = 10
def evlist_spe_hot(request):
    user = current_user(request)
    grouped_events = query.events_hot(SPE_LIMIT, rsvp_user=user)
    inner_html = render_to_string("cal/evlist_inner.html", {'grouped_events': grouped_events, 'evlist_show_date': True})
    out_dict = {
        'evlist_inner': inner_html,
        'evlist_title': "Hottest Upcoming Events",
    }
    return evlist_render_page(request, out_dict)

def evlist_spe_new(request):
    user = current_user(request)
    grouped_events = query.events_new(SPE_LIMIT, rsvp_user=user)
    inner_html = render_to_string("cal/evlist_inner.html", {'grouped_events': grouped_events, 'evlist_show_date': True})
    out_dict = {
        'evlist_inner': inner_html,
        'evlist_title': "Newest Upcoming Events",
    }
    return evlist_render_page(request, out_dict)

def evlist_spe_myviewed(request):
    user = current_user(request)
    grouped_events = query.events_myviewed(user, SPE_LIMIT, rsvp_user=user)
    inner_html = render_to_string("cal/evlist_inner.html", {'grouped_events': grouped_events, 'evlist_show_date': True})
    out_dict = {
        'evlist_inner': inner_html,
        'evlist_title': "Events I've Viewed",
    }
    return evlist_render_page(request, out_dict)


def evlist_parse_time_params(request):
    """Parse timeselect params from the GET request headers"""
    time_params = {'show': True}

    if "ts" in request.GET:
        timeselect = request.GET['ts']
    else:
        timeselect = "upcoming"
    time_params['ts'] = timeselect

    if timeselect == "upcoming":
        start_day = datetime.now()
    else:
        if "sd" in request.GET:
            sd = request.GET['sd']
            sd_y = int(sd[0:4])
            sd_m = int(sd[4:6])
            sd_d = int(sd[6:8])
            start_day = datetime(sd_y, sd_m, sd_d, 0, 0, 0)
        else:
            td = datetime.today()
            start_day = datetime(td.year, td.month, td.day, 0, 0, 0)
    ts_ind, start_day, end_day = query.get_sded(timeselect, start_day)
    end_day_show = end_day - timedelta(days=1) #since we want to display inclusive dates; otherwise we're showing [inclusive exclusive]
    time_params['sd'] = start_day.strftime("%Y%m%d")
    time_params['ed'] = end_day_show.strftime("%Y%m%d")

    if ts_ind == 0:
        title = "Upcoming Events"
        dates_title = "%s - %s" % (
            cal_util.strftime_yearopt(start_day, "%a, %b %e"),
            cal_util.strftime_yearopt(end_day_show, "%a, %b %e"))
    else:
        title = "Events - %s" % timeselect.capitalize()
        if ts_ind == 1:
            dates_title = cal_util.strftime_yearopt(start_day, "%A, %B %e")
        elif ts_ind == 2:
            dates_title = "Week of %s" % start_day.strftime("%B %e, %Y")
        elif ts_ind == 3:
            dates_title = "Month of %s" % start_day.strftime("%B %Y")

    return time_params, title, dates_title, start_day, end_day

def evlist_parse_filter_params(request):
    """Parse event filter params from the GET request headers"""
    filter_params = {'show': True}

    if "query" in request.GET:
        query_string = request.GET['query']
        query_string_fmt = query_string.strip().split(",")
        query_words = []
        for entry in query_string_fmt:
            query_words += entry.split(" ")
        filter_params['query'] = query_string
    else:
        query_words = None

    if "tag" in request.GET:
        tags = request.GET.getlist('tag')
        filter_params['tags'] = tags
    else:
        tags = None

    if "feat" in request.GET:
        feat_ids = map(int, request.GET.getlist('feat'))
        filter_params['feats'] = feat_ids
    else:
        feat_ids = None

    if "creator" in request.GET:
        creator = request.GET['creator']
        filter_params['creator'] = creator
    else:
        creator = None

    return filter_params, query_words, tags, feat_ids, creator


def evlist_render_page(request, out_dict):
    q_upcoming = query.query_upcoming()

    # Posters on top
    out_dict['poster_events'] = Event.objects.filter(q_upcoming, event_cluster__cluster_image__isnull=False).exclude(event_cluster__cluster_image='').order_by('event_date_time_start')[0:7]
    out_dict['hotest_events'] = Event.objects.filter(q_upcoming, event_cluster__cluster_image__isnull=False, event_attendee_count__gte=1).exclude(event_cluster__cluster_image='').order_by('-event_attendee_count')[0:7]

    # Features: just show all
    feat_list = EventFeature.objects.all()
    out_dict['feat_opts'] = feat_list    

    return render_to_response(request, "cal/evlist.html", out_dict)


@login_required
def confirm(request, event_id):
    try:
        event = Event.objects.get(event_id = event_id)
    except:
        return go_back(request,'That event could not be found.',0)    
    user = current_user(request)
    referrer = None
    reminder = True
    confirm_attendance(user,referrer,event,reminder).push(request)
    return HttpResponseRedirect('/events/%s' % (event_id));


@login_required
def unconfirm(request, event_id):
    user = current_user(request)
    try:
        event = Event.objects.get(event_id = event_id)
    except:
        return go_back(request,'That event could not be found.',0)
    unconfirm_attendance(user,event).push(request)
    return HttpResponseRedirect('/events/%s' % (event_id))


@login_required
def events_description(request, event_id):
    myEvent = Event.objects.get(event_id=event_id)
    myEvent.event_attendee_count = myEvent.getAttendeeCount()
    myEvent.save()
    
    associatedEvents = Event.objects.exclude(event_date_time_start=dtdeleteflag).filter(event_cluster = myEvent.event_cluster).exclude(pk=myEvent.pk).order_by('event_date_time_start')
    boardMessages = BoardMessage.objects.filter(boardmessage_eventcluster = myEvent.event_cluster).order_by('boardmessage_time_posted').reverse()
    dict = {'event': myEvent, 'associatedEvents': associatedEvents, 'boardMessages': boardMessages}

    try:
        dict['prev_event'] = myEvent.getPrevEvent()
    except:
        pass
    try:
        dict['next_event'] = myEvent.getNextEvent()
    except:
        pass
    try:
        dict['conc_events'] = myEvent.getConcurrentEvents()
    except:
        pass
        
    if request.method == 'GET' and 'forwardtoevents' in request.GET:
        dict['forwardtoevents'] = True
    else:
        dict['forwardtoevents'] = False
        
    public_guests = RSVP.objects.filter(rsvp_event = myEvent, rsvp_type = 'Accepted', rsvp_user__user_privacy_enabled = False).order_by('rsvp_user__user_netid')
    private_guests = RSVP.objects.filter(rsvp_event = myEvent, rsvp_type = 'Accepted', rsvp_user__user_privacy_enabled = True).order_by('rsvp_user__user_netid')
    
    user = current_user(request)
    dict['authorized'] = myEvent.isAuthorizedModifier(user)        
    
    n_public_guests = public_guests.count()
    
    max_disp = 5;
    
    if n_public_guests > max_disp+1:
        dict['whoscoming'] = public_guests[0:max_disp]
        dict['whoscoming_extra'] = (n_public_guests - max_disp) + private_guests.count()
        dict['show_extra'] = True
    else:
        dict['whoscoming'] = public_guests
        dict['whoscoming_extra'] =  private_guests.count()
        dict['show_extra'] = False
        

    if dict['authorized']:
        dict['whoscoming'] = RSVP.objects.filter(rsvp_event = myEvent, rsvp_type = 'Accepted').order_by('rsvp_user__user_netid')
        dict['whoscoming_extra'] = 0
        dict['show_extra'] = False
        
    user.add_viewed(myEvent)

    dict['open_invites'] = RSVP.objects.filter(rsvp_event = myEvent, rsvp_type = 'Pending').count()

    try: 
        previous_view = View.objects.get(view_viewer = user, view_event = myEvent)
        previous_view.view_count = previous_view.view_count + 1
        previous_view.view_date_time = datetime.now()
        previous_view.save()
    except:
        new_view = View(view_event = myEvent, 
                view_date_time = datetime.now(),
                view_viewer=user, 
                view_count = 1)
        new_view.save()
    try: 
        dict['users_rsvp'] = RSVP.objects.get(rsvp_user = user, rsvp_event = myEvent)
        if 'showrsvp' in request.GET:
            Msg('%s has invited you to this event. <a href="/user/invitations/%s/accept/">Accept?</a> <a href="/user/invitations/%s/decline/">Decline?</a> ' % (dict['users_rsvp'].rsvp_referrer.full_name(),dict['users_rsvp'].pk,dict['users_rsvp'].pk),1).push(request)
    except:
        pass
        # dict['unrsvp_url'] = '/events/%s/unconfirm' % (event_id)
        
    try:
        address = urllib.quote('%sevents/%s' % (our_site, event_id), safe='')
        dict['bitly_address'] = urllib.urlopen('http://api.bit.ly/v3/shorten?login=princetoneventscalendar&apiKey=R_16e331c21bf86e1f97667dec5608dba6&longUrl=%s&format=txt' % address).readlines()[0]
    except:
        dict['bitly_address'] = 'none'
    
    return render_to_response(request,"cal/events_description.html", dict)

    
@login_required
def board_message(request):
    if request.method == 'POST':
        message_title = 'unusued'
        message_body = request.POST.get('message_body',None)
        event_id = request.POST.get('event_id',None)
        user = current_user(request)
        if message_body and event_id and user:
            try:
                myEvent = Event.objects.get(event_id=event_id)
            except:
                return go_back(request,'Malformed message posting. Something is missing',0)
            event_cluster = myEvent.event_cluster
            send_message(user,event_cluster,message_title,message_body).push(request)
            if event_cluster.cluster_user_created != user:
                email_board_message(event_cluster.cluster_user_created, user, myEvent, message_body)
            return HttpResponseRedirect('/events/%s' % event_id)
        else:
            return go_back(request,'Malformed message posting. Something is missing.',0)
    else:
        return go_back(request,'Malformed message posting. You must submit using the proper form.',0)

@login_required
def delete_bmsg(request, bmsg_id):
    try:
        myBMessage = BoardMessage.objects.get(pk = bmsg_id)
        if current_user(request) == myBMessage.boardmessage_poster:
            myBMessage.delete()
            return go_back(request,"You've successfully deleted a message from the discussion board.",1)
        else:
            return go_back(request,"You are not authorized to delete this message.",0)
    except:
        return go_back(request,"I\'m sorry, but that is an illegal action.",0)
        
@login_required
def report_bmsg(request, bmsg_id):
    myBMessage = BoardMessage.objects.get(pk = bmsg_id)
    message = "The following message on PCal was just reported: "
    message = message+str(myBMessage)+"\n\n"
    message = message+"It was posted by: "+myBMessage.getPoster()+" on "+myBMessage.getFormattedTimePosted()+" at "+myBMessage.getTime()+".\n\n"
    message = message+"\nThis is a link to the page where the message was posted:\n\n"
    message = message+our_site
    myCluster = myBMessage.boardmessage_eventcluster
    myEvents = Event.objects.filter(event_cluster = myCluster)
    if myEvents:
        myEvent = myEvents[0]
        myEventUrl = myEvent.get_absolute_url()
        message = message+myEventUrl
    send ("usg@princeton.edu", "usg@princeton.edu", "Princeton Events Calendar: Board Message Reported", message)
    return go_back(request,'A report about this board message was sent to the website administrator. Thank you.',1)


@login_required
def invite(request):
    if request.method == 'POST':
        invitee = request.POST.get('invitee',None)
        event_id = request.POST.get('event_id',None)
        try:
            invitee_u = CalUser.objects.get(user_netid = invitee)
        except:
            if gdi(invitee):
                invitee_u = make_new_user(invitee)
                Msg('%s is new to the calendar, so an account was created.' % (invitee_u.full_name()),1).push(request)
            else:    
                return go_back(request,'The person with netid \'%s\' seems not to exist. Please enter a netid only.' % (cgi.escape(invitee)),0)
        user = current_user(request)
        if invitee_u and event_id and user:
            try:
                event = Event.objects.get(event_id=event_id)
            except:
                return go_back(request,'A corresponding event could not be found.',0)
            send_invite(user,invitee_u,event).push(request)
            return HttpResponseRedirect('/events/%s' % event_id)
        else:
            Msg('Malformed invitation. Something is missing',0).push(request)
        if invitee:
            Msg('Invitee is here.',0).push(request)
        if event_id:
            Msg('Event ID is here.',0).push(request)
        if user:
            Msg('User is here.',0).push(request)
        return go_back(request,'There was a problem.',0)
    else:
        return go_back(request,'Malformed invitation. You must send invitations using the proper form.',0)

@login_required
def invite_response(request,invite_id,action):
    try:
        rsvp = RSVP.objects.get(pk = invite_id)
        if rsvp.rsvp_user != current_user(request):
            return go_back(request,'Operation not permitted by your current user account.',0)
    except:
        return go_back(request,'Illegal operation. That invitation could not be found.',0)
    if action == 'accept':
        accept_invitation(rsvp).push(request)
        return HttpResponseRedirect('/events/%s' % (rsvp.rsvp_event.event_id))
    elif action == 'decline':
        decline_invitation(rsvp).push(request)
        return HttpResponseRedirect('/events/%s' % (rsvp.rsvp_event.event_id))
    else:
        return go_back(request,'Illegal operation.',0)
        
@login_required
def events_forwardtocampusevents(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id',None)
        custommsg = request.POST.get('message','<No message entered by user>')
        user = current_user(request)
        try:
            event = Event.objects.get(event_id=event_id)
        except:
            return go_back(request,'A corresponding event could not be found.',0)
        if event.isAuthorizedModifier(user):    
            email_forwardtocampusevents(user,event,custommsg)
            Msg('Your request was sent successfully',1).push(request)
            return HttpResponseRedirect('/events/%s' % (event.event_id))
        else:
            return go_back(request,'You are not authorized to submit this.',0)
    else:
        return go_back(request,'Invalid request.',0)


@login_required
def events_add(request):
    user = current_user(request)
    EventFormSet = formset_factory(EventForm, formset=RequiredFormSet)

    if request.method == 'POST':
        tags_in = request.POST['cluster_tags']
        request.POST['cluster_tags'] = []
        formset = EventFormSet(request.POST, request.FILES)
        clusterForm = EventClusterForm(request.POST, request.FILES)
        if formset.is_valid() and clusterForm.is_valid():
            new_cluster = clusterForm.save(commit=False)
            new_cluster.cluster_user_created = user
            new_cluster.save()
            clusterForm.save_m2m()
            tag_names = json.loads(tags_in)
            for tag_name in tag_names:
                try:
                    tag = EventCategory.objects.get(category_name=tag_name)
                except EventCategory.DoesNotExist:
                    tag = EventCategory(category_name=tag_name)
                    tag.save()
                new_cluster.cluster_tags.add(tag)
            new_cluster.save()
       
            for form in formset.forms:
                new_event = form.save(commit=False)
                new_event.event_cluster = new_cluster
                new_event.event_user_last_modified = user
                new_event.event_attendee_count = 0
                new_event.save()
                email_creator(user,new_event)

            # Added for interfacing with Student Groups
            if 'post_groups' in request.POST and request.POST['post_groups']:
                group = Group.objects.get(id=request.POST['post_groups'])
                entry = Entry(title=new_cluster.cluster_title,text='',event=new_event,group=group)
                entry.save()
                mships = Membership.objects.filter(group=group,feed_notifications=True)
                list = []
                for m in mships:
                    list.append(str(m.student.email))
                    send_mail(EMAIL_HEADER_PREFIX+'\"%s\" Posted to its Feed'%group.name, FEED_NOTIFICATION_EMAIL % (group.name,entry.title,entry.text,group.url), SITE_EMAIL, list, fail_silently=False)

            if 'submit' in request.POST:
                return HttpResponseRedirect('/events/%s?forwardtoevents' % (new_event.event_id))

    else:   
        formset = EventFormSet()
        clusterForm = EventClusterForm()

    try:
        most_recent_submission = Event.objects.filter(event_cluster__cluster_user_created=user).latest('event_cluster__cluster_date_time_created')
        if datetime.now() - most_recent_submission.event_cluster.cluster_date_time_created <= timedelta(minutes=240):
             Msg('You just submitted \'<a href="/events/%s">%s</a>\'. Are you adding another date/time for this event or another in this series?<br />Consider adding a <a href="/events/add/%s">related event here</a> instead of a brand new one below.' % (most_recent_submission.pk,most_recent_submission.displayname(),most_recent_submission.pk),2).push(request)
    except:
        pass

    # data for interfacing with Student Groups
    group = None
    group_mships = Membership.objects.filter(student__netid__exact=user.user_netid,type='O')
    if not group_mships.count():
        try:
            group = Group.objects.get(netid__exact=user.user_netid)
        except:
            pass
    tag_opts = [tag.category_name for tag in EventCategory.objects.all().order_by('category_name')]
    tag_sugs = json.dumps(tag_opts)
    return render_to_response(request, 'cal/events_add.html', {
        'formset': formset,
        'clusterForm': clusterForm,
        'group_mships':group_mships,
        'group':group,
        'tag_sugs':tag_sugs
    })


@login_required
def events_add_another(request, event_id):
   base_event = Event.objects.get(event_id = event_id)
   base_cluster = base_event.event_cluster
   EventFormSet = formset_factory(EventForm, extra=0, formset=RequiredFormSet)

   if request.method == 'POST':
      formset = EventFormSet(request.POST)
      user = request.session.get('user_data',None)
      #eventForm = EventForm(request.POST)
      if formset.is_valid():
         for eventForm in formset.forms:
            new_event = eventForm.save(commit=False)
            new_event.event_cluster = base_cluster
            new_event.event_user_last_modified = user
            new_event.event_attendee_count = 0
            new_event.save()
            email_creator(user,new_event)

         if 'submit' in request.POST:
            #request.session['umessage'] = 'Event just added!'
            return HttpResponseRedirect('/events/%s?forwardtoevents' % (new_event.event_id))
   else:
      #eventForm = EventForm(instance=base_event)
      formset = EventFormSet(initial=[{'event_subtitle': base_event.event_subtitle, 'event_subdescription': base_event.event_subdescription, 'event_date_time_start': base_event.event_date_time_start, 'event_date_time_end': base_event.event_date_time_end, 'event_location': base_event.event_location, 'event_location_details': base_event.event_location_details, 'event_date_rsvp_deadline': base_event.event_date_rsvp_deadline, 'event_max_attendance': base_event.event_max_attendance}])

    #dict = {'cluster': base_cluster, 'eventForm': eventForm }
   return render_to_response(request, 'cal/events_add.html', {'formset':formset, 'event':base_event})


@login_required
def events_manage_ID(request, event_ID):
   thisEvent = Event.objects.get(event_id=event_ID)
   
   if not thisEvent.isAuthorizedModifier(current_user(request)):
      return go_back(request,'Only an event administrator can modify the event.',0)
   
   if Event.objects.filter(event_cluster = thisEvent.event_cluster).count() > 1:
      multiDay = True
   else:
      multiDay = False
      
   if request.method =='POST':
      if 'submit' in request.POST or 'submitnonotify' in request.POST:
         clusterForm = EventClusterForm(request.POST, request.FILES, instance = thisEvent.event_cluster)
         if multiDay:
            eventForm = EventForm(request.POST, instance=thisEvent)
         else:
            eventForm = SingleEventForm(request.POST, instance=thisEvent)
            
         if eventForm.is_valid() and clusterForm.is_valid():
            modifier = current_user(request)
            eF = eventForm.save(commit=False)
            eF.event_user_last_modified = modifier
            eF.save()
            cF = clusterForm.save()
            Msg('The event was successfully updated.',1).push(request)
            if not 'submitnonotify' in request.POST:
                rsvps = RSVP.objects.filter(rsvp_event = eF).filter(rsvp_type = 'Accepted')
                for rsvp in rsvps:
                   user = rsvp.rsvp_user
                   email_event_modification(user, modifier, eF)
                Msg('Number of notification emails sent: %s' % (len(rsvps)),1).push(request)
            else:
                Msg('No attendees were notified.',1).push(request)
            return HttpResponseRedirect('/events/%s' % (eF.event_id))
      elif 'cancel' in request.POST:
          thisEvent.cancelled = True
   else:
      if multiDay:
         eventForm = EventForm(instance=thisEvent)
      else:
         eventForm = SingleEventForm(instance=thisEvent)
      clusterForm = EventClusterForm(instance=thisEvent.event_cluster)
   
   dict = {'eventForm':eventForm, 'clusterForm':clusterForm, 'event':thisEvent}

   return render_to_response(request, 'cal/events_manage.html', dict )


@login_required
def events_cancel(request, event_ID):
   Msg('Canceled events will still remain in the upcoming events list but appear with a strikethrough. Upon cancellation, all attendees will be notified by email.  If you made a mistake that you would like to correct, choose "<a href="/events/manage/%s">Modify this event</a>" instead.<br /><br />Are you sure you wish to cancel this event?<br /><a href="/events/cancel_confirm/%s">Yes, permanently cancel this event.</a> &nbsp;&nbsp;<a href="/events/%s">No, do not cancel ths event.</a>' % (event_ID, event_ID, event_ID),0).push(request)
   return HttpResponseRedirect('/events/%s' % (event_ID))
   
@login_required
def events_cancel_confirm(request, event_ID):
   try:
      event = Event.objects.get(event_id=event_ID)
   except:
      return go_back(request,'Error: Event not found',0)
   modifier = current_user(request)
   if event.isAuthorizedModifier(modifier):    
      event.event_cancelled = True
      event.save()
      rsvps = RSVP.objects.filter(rsvp_event = event).filter(rsvp_type = 'Accepted')
      
      for rsvp in rsvps:
         user = rsvp.rsvp_user
         #if user != modifier:
         email_event_cancellation(user, modifier, event)
      return go_back(request,'This event was permanently cancelled.',1)
   else:
      return go_back(request,'You are not authorized to cancel this event.',0) 

@login_required
def events_delete(request, event_ID):
   Msg('Deleted events will be removed permanently from the calendar system. Upon cancellation, all attendees will be notified by email.  If you made a mistake that you would like to correct, choose "<a href="/events/manage/%s">Modify this event</a>" instead.<br /><br />Are you sure you wish to delete this event?<br /><a href="/events/delete_confirm/%s">Yes, permanently delete this event.</a> &nbsp;&nbsp;<a href="/events/%s">No, do not delete ths event.</a>' % (event_ID, event_ID, event_ID),0).push(request)
   return HttpResponseRedirect('/events/%s' % (event_ID))

@login_required
def events_delete_confirm(request, event_ID):
   try:
      event = Event.objects.get(event_id=event_ID)
   except:
      return go_back(request,'Error: Event not found',0)
   modifier = current_user(request)
   if event.isAuthorizedModifier(modifier):    
      event.event_cancelled = True
      event.event_date_time_start = dtdeleteflag
      event.event_date_time_end = dtdeleteflag
      event.save()
      rsvps = RSVP.objects.filter(rsvp_event = event).filter(rsvp_type = 'Accepted')
      
      for rsvp in rsvps:
         user = rsvp.rsvp_user
         #if user != modifier:
         email_event_cancellation(user, modifier, event)
      return go_back(request,'This event was permanently deleted.',1)
   else:
      return go_back(request,'You are not authorized to delete this event.',0) 

@login_required
def showQR(request, event_id):
    try:
        myEvent = Event.objects.get(event_id=event_id)
    except:
        return go_back(request, 'Error: No event found',0)
    user = current_user(request)
    dict = {'event': myEvent}
    dict['tabtitle'] = 'Quick Response Code'
    dict['user'] = user
    dict['personal_link'] = '%sbulkinvite/%s-%s-p' % (our_site, myEvent.pk, user.pk)
    personallongencoded = urllib.urlencode({'login':'princetoneventscalendar',
                                            'apiKey':'R_16e331c21bf86e1f97667dec5608dba6',
                                            'longUrl':dict['personal_link'],
                                            'format':'txt',})
    bitlylink = 'http://api.bit.ly/v3/shorten?%s' % (personallongencoded)
    dict['personalqr_link'] = urllib.urlopen(bitlylink).readlines()[0]
    personalqrparams = urllib.urlencode({    's':'8',
                                            't':'p',
                                            'd':dict['personalqr_link'],})
    dict['personalqr_url'] = 'http://qrcode.kaywa.com/img.php?%s' % (personalqrparams)
    dict['generalqr_link'] = '%sevents/%s' % (our_site, myEvent.pk)
    generalqrparams = urllib.urlencode({    's':'8',
                                            't':'p',
                                            'd':dict['generalqr_link'],})
    dict['generalqr_url'] = 'http://qrcode.kaywa.com/img.php?%s' % (generalqrparams)
    return render_to_response(request,"cal/qr_code.html", dict)
    

@login_required    
def custom_invite_message(request, event_id):
    try:
        myEvent = Event.objects.get(event_id=event_id)
    except:
        return go_back(request, 'Error: No event found',0)
    user = current_user(request)
    if not myEvent.isAuthorizedModifier(user):
        Msg('Only an event administrator can use this feature to send invitations to a list.',0).push(request)
        return HttpResponseRedirect('/events/%s' % event_id)
    else:
        dict = {'event': myEvent}
        dict['flag_custom_invite'] = True
        return render_to_response(request,"cal/email_attendees.html", dict)

@login_required    
def custom_invite_message_sent(request, event_id):
    if request.method == 'POST':
        myEvent = Event.objects.get(event_id=event_id)
        user = current_user(request)
        if not myEvent.isAuthorizedModifier(user):
            return go_back(request, 'You are not authorized to complete this action.',0)
        message_from = request.POST.get('from',None)
        if not message_from:
            return go_back(request, 'You must provide a valid "from" address.',0)
        message_to = request.POST.get('to',None)
        if not message_to:
            return go_back(request, 'You must provide a valid "to" address.',0)
        message_title = request.POST.get('subject',None)
        message_body = request.POST.get('message',None)
        return email_custom_invitation(request, myEvent, message_from, message_to, message_title, message_body)
    else:
        return go_back(request, 'Invalid request.',0)    

@login_required
def bulk_invite_response(request, event_id, sender_id, response):
    try:
        event = Event.objects.get(pk = event_id)
    except:
        return go_back(request, 'Invalid event number.',0)
    try:
        inviter = CalUser.objects.get(pk = sender_id)
    except:
        return go_back(request, 'Invalid user.',0)
    user = current_user(request)
    try:
        existing_rsvp = RSVP.objects.get(rsvp_user=user, rsvp_event=event)
        if existing_rsvp.rsvp_type == 'Accepted':
            if response == 'a':
                Msg('You have already confirmed your attendance for this event.',0).push(request)
            elif response == 'd':
                decline_invitation(existing_rsvp).push(request)
            else:
                pass
        elif existing_rsvp.rsvp_type == 'Pending':
            if response == 'a':
                accept_invitation(existing_rsvp).push(request)
            elif response == 'd':
                decline_invitation(existing_rsvp).push(request)
            else:
                pass        
        else:
            if response == 'a':
                Msg('You have already declined attendance for this event. Would you like to <a href="/user/invitations/%s/accept/">change your mind</a>?' % (existing_rsvp.pk),0).push(request)                
            elif response == 'd':
                Msg('You have already declined attendance for this event.',0).push(request)                
            else:
                pass
    except:
        rsvp = RSVP(rsvp_user = current_user(request),
                    rsvp_referrer = inviter,
                    rsvp_event = event,
                    rsvp_reminder_enabled = True,
                    rsvp_type='Pending')
        rsvp.save()
        if response == 'a':
            accept_invitation(rsvp).push(request)    
        elif response == 'd':
            decline_invitation(rsvp).push(request)
        elif response == 'p':
            return HttpResponseRedirect('/events/%s?showrsvp=true' % event_id)
        else:
            return go_back(request, 'Invalid status.',0)
    return HttpResponseRedirect('/events/%s' % event_id)

    
@login_required
def ical(request, event_id):
   event = Event.objects.get(event_id=event_id)
   cal = vobject.iCalendar()
   cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this
   
   vevent = cal.add('vevent')
   vevent.add('summary').value = str(event)
   vevent.add('dtstart').value = event.event_date_time_start
   vevent.add('dtend').value = event.event_date_time_end

   vevent.add('location').value = event.getGCalLocation()
   vevent.add('description').value = event.getGCalClusterDes() + "\n\n" + event.getGCalEventDes()

   icalstream = cal.serialize()
   response = HttpResponse(icalstream, mimetype='text/calendar')
   response['Filename'] = 'pcal.ics'  # IE needs this
   response['Content-Disposition'] = 'attachment; filename=pcal.ics'
   return response


#Feeds
def feedLanding(request, name, description):
    dict = {}
    dict['http_feed_continue'] = request.build_absolute_uri()
    dict['webcal_feed_continue'] = request.build_absolute_uri().replace('http://','webcal://')
    dict['tabtitle'] = 'Live Feed: \'%s\'' % (name)
    dict['feed_name'] = name
    dict['feed_desc'] = description
    return render_to_response(request,"cal/feed_landing.html", dict)

def feedRedirect(request):
    #Msg('ct: %s' % request.build_absolute_uri(),0).push(request)
    if request.build_absolute_uri().find('webcal://') == 0:
        return False
    ref = request.META.get('HTTP_REFERER',None)
    #Msg('Ref: %s' % ref,0).push(request)
    
    if ref and ref.find(our_site) == 0:
        ref_path = ref.replace(our_site,'/')
        #Msg('Ref_path: %s' % ref_path,0).push(request)
        cur = request.path
        #Msg('cur: %s' % cur,0).push(request)
        if ref_path != cur:
            return True
        else:
            return False
    else:
        return False
    

def feedByTags(request, category):
    try:
        filter_cat = EventCategory.objects.get(category_name=category)
    except:
        return go_back(request, 'Invalid category.',0)
    name = "'%s' Events" % (category);
    description = "Live Feed: Events in the category '%s' posted on the Princeton Events Calendar, a service of the Princeton USG. For the full calendar, visit %s." % (category, our_site);
    if feedRedirect(request):
        return feedLanding(request, name, description)
    events = Event.objects.exclude(event_date_time_start=dtdeleteflag).filter(event_cluster__cluster_tags=filter_cat)
    return generateFeed(events, name, description)
    
def feedByFeature(request, feature):
    try:
        filter_feat = EventFeature.objects.get(feature_name=feature)
    except:
        return go_back(request, 'Invalid feature.',0)
    name = "'%s' Events" % (feature);
    description = "Live Feed: Events featuring '%s' posted on the Princeton Events Calendar, a service of the Princeton USG. For the full calendar, visit %s." % (feature, our_site);
    if feedRedirect(request):
        return feedLanding(request, name, description)
    events = Event.objects.exclude(event_date_time_start=dtdeleteflag).filter(event_cluster__cluster_features=filter_feat)
    return generateFeed(events, name, description)    
    
def feedByUser(request, user):
    try:
        filter_user = CalUser.objects.get(user_netid=user)
    except:
        return go_back(request, 'Invalid user.',0)
    name = "Events by %s" % (filter_user.full_name_suffix());
    description = "Live Feed: Events posted by '%s' to the Princeton Events Calendar, a service of the Princeton USG. For the full calendar, visit %s." % (filter_user.full_name_suffix(), our_site);
    if feedRedirect(request):
        return feedLanding(request, name, description)
    events = Event.objects.exclude(event_date_time_start=dtdeleteflag).filter(event_cluster__cluster_user_created=filter_user)
    return generateFeed(events, name, description)        

def feedAllEvents(request):
    name = "All Campus Events"
    description = "Live Feed: All upcoming events posted to the Princeton Events Calendar, a service of the Princeton USG. For the full calendar, visit %s." % our_site
    if feedRedirect(request):
        return feedLanding(request, name, description)
    events = Event.objects.exclude(event_date_time_start=dtdeleteflag).filter(event_date_time_start__gte=datetime.now())
    return generateFeed(events, name, description)
    
def feedMyEvents(request, id, netid):
    user = CalUser.objects.get(pk=id)
    check = CalUser.objects.get(user_netid=netid)
    
    if user != check:
        return go_back(request, 'Malformed link.',0)
        
    name = 'My Campus Events'
    description = "Live Feed: %s's personal events on the Princeton Events Calendar. Includes events to which you confirmed attendance for synchronizing with your personal calendar program. Set your calendar program to synchronize this feed at least hourly for best accuracy. Keep this link private. For the full calendar, visit %s." % (user.full_name(), our_site)
    if feedRedirect(request):
        return feedLanding(request, name, description)
    rsvps = RSVP.objects.exclude(rsvp_event__event_date_time_start=dtdeleteflag).filter(rsvp_user=user,rsvp_type='Accepted')
    events = []
    for rsvp in rsvps:
        events.append(rsvp.rsvp_event)
    return generateFeed(events, name, description)

def generateFeed(events, name, description):
    cal = vobject.iCalendar()
    cal.add('CALSCALE').value = 'GREGORIAN'
    cal.add('METHOD').value = 'PUBLISH'
    cal.add('X-WR-CALNAME').value = name
    cal.add('X-WR-TIMEZONE').value = 'America/New_York'
    cal.add('X-WR-CALDESC').value = description
    
    for event in events:
        vevent = cal.add('VEVENT')
        vevent.add('UID').value = "%i@%s" % (event.event_id, our_email)
        vevent.add('RELATED-TO').value = 'RELTYPE=CHILD:%irecur@%s' % (event.event_cluster.cluster_id, our_email)
        vevent.add('SUMMARY').value = smart_unicode(str(event))
        vevent.add('DTSTART').value = event.event_date_time_start
        vevent.add('DTEND').value = event.event_date_time_end
        vevent.add('CREATED').value = event.event_cluster.cluster_date_time_created
        vevent.add('LAST-MODIFIED').value = event.event_date_time_last_modified
        if event.event_cancelled == True:
            vevent.add('STATUS').value = "CANCELLED"
        else:
            vevent.add('STATUS').value = "CONFIRMED"
        vevent.add('URL').value = event.get_absolute_url()
        vevent.add('TRANSP').value = 'TRANSPARENT'
        vevent.add('ORGANIZER').value = '%s' % (event.event_cluster.cluster_user_created.user_email)
        
        vevent.add('LOCATION').value = unicode(event.getGCalLocation())
        vevent.add('DESCRIPTION').value = unicode(event.getGCalClusterDes() + "\n\n" + event.getGCalEventDes())

    icalstream = cal.serialize()
    response = HttpResponse(icalstream, mimetype='text/calendar')
    response['Content-Type'] = 'text/calendar; charset=utf-8'
#     response['Transfer-Encoding'] = 'chunked'
    response['Connection'] = 'close'
    response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
    response['Pragma'] = 'no-cache'
    return response    

def icalFeed(request, tag):
    cal = vobject.iCalendar()
    cal.add('CALSCALE').value = 'GREGORIAN'
    cal.add('METHOD').value = 'PUBLISH'
    cal.add('X-WR-CALNAME').value = tag + ' Events'
    cal.add('X-WR-TIMEZONE').value = 'America/New_York'
    cal.add('X-WR-CALDESC').value = 'Calendar of campus events. Filter:'+tag
    
    filteredEvents = Event.objects.filter(event_date_time_end__lte=datetime.now()).order_by('event_date_time_start')
    if not tag == "All":
        filteredEvents = filteredEvents.filter(event_cluster__cluster_tags__category_name=tag)
    
    for event in filteredEvents[0:200]:
        vevent = cal.add('VEVENT')
        vevent.add('SUMMARY').value = smart_unicode(str(event))
        vevent.add('DTSTART').value = event.event_date_time_start
        vevent.add('DTEND').value = event.event_date_time_end
        
        vevent.add('LOCATION').value = unicode(event.getGCalLocation())
        vevent.add('DESCRIPTION').value = unicode(event.getGCalClusterDes() + "\n\n" + event.getGCalEventDes())

    icalstream = cal.serialize()
    response = HttpResponse(icalstream, mimetype='text/calendar')
    response['Content-Type'] = 'text/calendar; charset=utf-8'
#     response['Transfer-Encoding'] = 'chunked'
    response['Connection'] = 'close'
    response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
    response['Pragma'] = 'no-cache'
    return response

def subscribe(request, tag):
    cal = vobject.iCalendar()
    cal.add('CALSCALE').value = 'GREGORIAN'
    cal.add('METHOD').value = 'PUBLISH'
    cal.add('X-WR-CALNAME').value = tag + ' Events'
    cal.add('X-WR-TIMEZONE').value = 'America/New_York'
    cal.add('X-WR-CALDESC').value = 'Calendar of campus events. Filter:'+tag
    cal.add('X-PUBLISHED-TTL').value = 'PT60M'
    
    filteredEvents = Event.objects.order_by('event_date_time_start')
    if not tag == "All":
        filteredEvents = filteredEvents.filter(event_cluster__cluster_tags__category_name=tag)

    for event in filteredEvents:
        vevent = cal.add('VEVENT')
        vevent.add('UID').value = "%i@%s" % (event.event_id, our_email)
        vevent.add('RELATED-TO').value = 'RELTYPE=CHILD:%irecur@%s' % (event.event_cluster.cluster_id, our_email)
        vevent.add('SUMMARY').value = smart_unicode(str(event))
        vevent.add('DTSTART').value = event.event_date_time_start
        vevent.add('DTEND').value = event.event_date_time_end
        vevent.add('CREATED').value = event.event_cluster.cluster_date_time_created
        vevent.add('LAST-MODIFIED').value = event.event_date_time_last_modified
        if event.event_cancelled == True:
            vevent.add('STATUS').value = "CANCELLED"
        else:
            vevent.add('STATUS').value = "CONFIRMED"
        vevent.add('URL').value = event.get_absolute_url()
        vevent.add('TRANSP').value = 'TRANSPARENT'
        vevent.add('ORGANIZER').value = '%s' % (event.event_cluster.cluster_user_created.user_email)
        
        vevent.add('LOCATION').value = unicode(event.getGCalLocation())
        vevent.add('DESCRIPTION').value = unicode(event.getGCalClusterDes() + "\n\n" + event.getGCalEventDes())
        


    icalstream = cal.serialize()
    response = HttpResponse(icalstream, mimetype='text/calendar')
    response['Content-Type'] = 'text/calendar; charset=utf-8'
    response['Connection'] = 'close'
    response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
    response['Pragma'] = 'no-cache'
    return response

def personalCalendar(request, id, netid):
    user = CalUser.objects.get(pk=id)
    check = CalUser.objects.get(user_netid=netid)
    
    if user != check:
        return
    
    cal = vobject.iCalendar()
    cal.add('CALSCALE').value = 'GREGORIAN'
    cal.add('METHOD').value = 'PUBLISH'
    cal.add('X-WR-CALNAME').value = 'My Campus Events'
    cal.add('X-WR-TIMEZONE').value = 'America/New_York'
    cal.add('X-WR-CALDESC').value = '%s\'s personal events from the Princeton Events Calendar, %s.' % (user.full_name(), our_site)
    cal.add('X-PUBLISHED-TTL').value = 'PT1H'
    
    
    userRSVPs = RSVP.objects.filter(rsvp_user=user,rsvp_type='Accepted').order_by('rsvp_event__event_date_time_start')

    for rsvp in userRSVPs:
        event = rsvp.rsvp_event
        vevent = cal.add('VEVENT')
        vevent.add('UID').value = "%i@%s" % (event.event_id, our_email)
        vevent.add('RELATED-TO').value = 'RELTYPE=CHILD:%irecur@%s' % (event.event_cluster.cluster_id, our_email)
        vevent.add('SUMMARY').value = smart_unicode(str(event))
        vevent.add('DTSTART').value = event.event_date_time_start
        vevent.add('DTEND').value = event.event_date_time_end
        vevent.add('CREATED').value = event.event_cluster.cluster_date_time_created
        vevent.add('LAST-MODIFIED').value = event.event_date_time_last_modified
        if event.event_cancelled == True:
            vevent.add('STATUS').value = "CANCELLED"
        else:
            vevent.add('STATUS').value = "CONFIRMED"
        vevent.add('URL').value = event.get_absolute_url()
        vevent.add('TRANSP').value = 'TRANSPARENT'
        vevent.add('ORGANIZER').value = '%s' % (event.event_cluster.cluster_user_created.user_email)
        
        vevent.add('LOCATION').value = unicode(event.getGCalLocation())
        vevent.add('DESCRIPTION').value = unicode(event.getGCalClusterDes() + "\n\n" + event.getGCalEventDes())
        


    icalstream = cal.serialize()
    response = HttpResponse(icalstream, mimetype='text/calendar')
    response['Content-Type'] = 'text/calendar; charset=utf-8'
    response['Connection'] = 'close'
    response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
    response['Pragma'] = 'no-cache'
    return response
    
def followCalendar(request, netid):
    user = CalUser.objects.get(user_netid=netid)
    
    cal = vobject.iCalendar()
    cal.add('CALSCALE').value = 'GREGORIAN'
    cal.add('METHOD').value = 'PUBLISH'
    cal.add('X-WR-CALNAME').value = '%s Events' % user.full_name()
    cal.add('X-WR-TIMEZONE').value = 'America/New_York'
    cal.add('X-WR-CALDESC').value = 'Events submitted by %s to the Princeton Events Calendar, %s.' % (user.full_name(), our_site)
    cal.add('X-PUBLISHED-TTL').value = 'PT1H'
    
    publishedEvents = Event.objects.filter(event_cluster__cluster_user_created=user).order_by('event_date_time_start')

    for event in publishedEvents:
        vevent = cal.add('VEVENT')
        vevent.add('UID').value = "%i@%s" % (event.event_id, our_email)
        vevent.add('RELATED-TO').value = 'RELTYPE=CHILD:%irecur@%s.' % (event.event_cluster.cluster_id, our_email)
        vevent.add('SUMMARY').value = smart_unicode(str(event))
        vevent.add('DTSTART').value = event.event_date_time_start
        vevent.add('DTEND').value = event.event_date_time_end
        vevent.add('CREATED').value = event.event_cluster.cluster_date_time_created
        vevent.add('LAST-MODIFIED').value = event.event_date_time_last_modified
        if event.event_cancelled == True:
            vevent.add('STATUS').value = "CANCELLED"
        else:
            vevent.add('STATUS').value = "CONFIRMED"
        vevent.add('URL').value = event.get_absolute_url()
        vevent.add('TRANSP').value = 'TRANSPARENT'
        vevent.add('ORGANIZER').value = '%s' % (event.event_cluster.cluster_user_created.user_email)
        
        vevent.add('LOCATION').value = unicode(event.getGCalLocation())
        vevent.add('DESCRIPTION').value = unicode(event.getGCalClusterDes() + "\n\n" + event.getGCalEventDes())

    icalstream = cal.serialize()
    response = HttpResponse(icalstream, mimetype='text/calendar')
    response['Content-Type'] = 'text/calendar; charset=utf-8'
    response['Connection'] = 'close'
    response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
    response['Pragma'] = 'no-cache'
    return response
    

def xml_feed(request):
    now = datetime.now()
    if 'from' in request.GET and 'to' in request.GET:
        from_time = request.GET['from']
        to_time = request.GET['to']
        from_split = from_time.split("-", 2)
        from_date = datetime(int(from_split[0]), int(from_split[1]), int(from_split[2]), 0, 0, 0)
        to_split = to_time.split("-", 2)
        to_date = datetime(int(to_split[0]), int(to_split[1]), int(to_split[2]), 23, 59, 59)
        eventList = Event.objects.filter(event_date_time_end__gte=from_date).filter(event_date_time_end__lte=to_date).order_by('event_date_time_start')
    else:
        eventList = Event.objects.filter(event_date_time_end__gte=datetime.now()).order_by('event_date_time_start')
        
    t = loader.get_template("cal/xml_feed.html")
    c = Context({'eventList': eventList, 'now': now})
    return HttpResponse(t.render(c),
            mimetype="text/xml")


def nocookie():
    dict = {}
    return render_to_response(request, 'cal/nocookie.html', dict)

@login_required
def feeds_tmp(request):
    user = current_user(request)
    return HttpResponseRedirect('/mycal/%d/%s.ics' % (user.pk, user.user_netid))

