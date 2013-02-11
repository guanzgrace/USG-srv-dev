################################################################
# Project: Princeton Events Calendar
# Authors: Ethan Goldstein, Samantha Hantman, Dana Hoffman, 
#		   Adriana Susnea, and Michael Yaroshefsky 
# Date:    May 11, 2010
################################################################
# Title:  urls.py
# Info :  the defined urls for this site
################################################################

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.http import HttpResponseRedirect

from views_events import *
from views_users import *
from csvdump import *
from attendee_email import *
from cal import rssfeed

admin.autodiscover()

OLD_FEEDS = {
    'latest': rssfeed.LatestEvents,
}

"""
replace:
cal/{{}} -> cal/gen/{{}}/
cal/upcoming -> cal/gen/upcoming/
all.ics -> feeds/all.ics

???????????????

feeds/
    feeds_index
    - make feeds/tag, feeds/user in feeds/ ***
feeds/all.ics, feeds/tag/{{}}.ics, feeds/user/{{}}.ics
    events_feed
eventsby/{{user}}.ics -> feeds/user/{{user}.ics
    feedByUser -> events_feed

eventsby/{{user}} -> cal/spec/user/{{}}/
    filterByUser
hotevents/ -> cal/spec/hot/
    showHotEvents
recentlyadded/ -> cal/spec/recentlyadded/
    showRecentlyAddedEvents
recentlyview/ -> cal/spec/recentlyviewed/
    showRecentlyViewedEvents
"""

urlpatterns = patterns('',
    # General listing of events
    (r'^/?$', lambda x: HttpResponseRedirect('/evlist/gen/')),
    (r'^evlist/gen/?$', 'cal.views_events.evlist_gen'),
    (r'^evlist/gen/ajax/?$', 'cal.views_events.evlist_gen_ajax'),
    (r'^evlist/spe/hot/?$', 'cal.views_events.evlist_spe_hot'),
    (r'^evlist/spe/new/?$', 'cal.views_events.evlist_spe_new'),
    (r'^evlist/spe/myviewed/?$', 'cal.views_events.evlist_spe_myviewed'),

    # Feeds
    (r'^feeds/?$', 'cal.views_events.feeds_index'),
    (r'^feeds/all.ics$', 'cal.views_events.events_feed'), #copy feedAllEvents, feedByUser
    (r'^feeds/tag/(?P<tag>[A-Za-z]+).ics$', 'cal.views_events.events_feed'),
    (r'^feeds/user/(?P<user>[A-Za-z]+).ics$', 'cal.views_events.events_feed'),

    # Feeds - old: Not sure how this one works
    (r'^feeds/(?P<url>.*)/?$', 'django.contrib.syndication.views.feed', {'feed_dict': OLD_FEEDS}),
    # Feeds - old: Not sure how this one works
    (r'^xml/?$', xml_feed),
    # Feeds - old: Need a redirect
    (r'^all.ics$', lambda x: HttpResponseRedirect('/feeds/all.ics')),

    # Authentication
    (r'^login/?$',login),
    (r'^logout/?$',logout),
    (r'^nocookie/?$',nocookie),

    # Event Description Page
    (r'^events/(?P<event_id>\d+)/?$',events_description),
    (r'^events/(?P<event_id>\d+)/confirm/?$',confirm),
    (r'^events/(?P<event_id>\d+)/unconfirm/?$',unconfirm),
    (r'^events/invite/?$',invite),
    (r'^events/board_message/?$',board_message),
    (r'^events/deletebmsg/(?P<bmsg_id>\d+)/?$', delete_bmsg),
    (r'^events/reportmsg/(?P<bmsg_id>\d+)/?$', report_bmsg),

    # Add Event Page
    (r'^events/add/?$',events_add),
    (r'^events/add/(?P<event_id>\d+)/?$', events_add_another),

    # Forward to campus events list
    (r'^events/forwardtocampusevents/?$', events_forwardtocampusevents),

    # Manage Event Page  (specific number of numbers?)
    (r'^events/manage/(?P<event_ID>\d+)/?$',events_manage_ID),

    # Cancel Event
    (r'^events/cancel/(?P<event_ID>\d+)/?$', events_cancel),
    (r'^events/cancel_confirm/(?P<event_ID>\d+)/?$', events_cancel_confirm),

    # Delete Event
    (r'^events/delete/(?P<event_ID>\d+)/?$', events_delete),
    (r'^events/delete_confirm/(?P<event_ID>\d+)/?$', events_delete_confirm),

    # Search Results
    #(r'^search/?$',events_search),

    # Manage Profile
    (r'^user/?$',user_profile),

    # My Events
    (r'^user/events/?$', user_upcoming_events),
    #<span id="no_upcoming">You have no upcoming events</span>

    # My Past Events
    (r'^user/oldevents/?$', user_past_events),

    # My Managed Events
    (r'^user/eventadmin/?$', user_admin_events),

    # Invitations
    (r'^user/invitations/?$',user_invitations),
    (r'^user/invitations/(?P<invite_id>\d+)/(?P<action>accept|decline)/?$',invite_response),
    (r'^bulkinvite/(?P<event_id>\d+)-(?P<sender_id>\d+)-(?P<response>a|d|p)/?$',bulk_invite_response),

    # Set Personal Alerts
    (r'^user/alerts/?$',user_alerts),
    (r'^user/messages/?$',user_messages),
    (r'^user/messages/hover.html$',user_messages_hover),

    # iCal   
    (r'^ical/(?P<event_id>\d+)/?$', ical),
    (r'^(?P<tag>.*)/subscription.ics$', icalFeed),
    (r'^subscribe/(?P<tag>.*).ics$', subscribe),
    (r'^mycal/(?P<id>\d+)/(?P<netid>.*).ics$', feedMyEvents),
    (r'^follow/(?P<netid>.*).ics$', followCalendar),

    # Send emails to attendees
    (r'^events/(?P<event_id>\d+)/sendmsg/?$', form_email_attendees),
    (r'^events/(?P<event_id>\d+)/msgsent/?$', email_attendees),

    # Get attendee list
    (r'^events/(?P<event_id>\d+)/attendees.csv$', downloadAttendeeList),

    # Send custom invitations
    (r'^events/(?P<event_id>\d+)/custominvite/?$', custom_invite_message),
    (r'^events/(?P<event_id>\d+)/custominvitesent/?$', custom_invite_message_sent),

    # QR Code
    (r'^events/(?P<event_id>\d+)/qr/?$', showQR),


    # Ajax goodness
    (r'^ajax/netidlookup/?$', 'cal.views_ajax.netidlookup'),
    (r'^ajax/allguests/?$', 'cal.views_ajax.allguests'),
    (r'^ajax/alltags/?$', 'cal.views_ajax.get_all_tags'),

    # I don't know what these do...
    (r'^test/adminfun/?$', 'cal.views_test.activityFeed'),
    (r'^test/lookup/?$', 'cal.views_test.userlookup'),

    # Admin - not upgradable since it doesn't use django_cas
    (r'^admin/', include(admin.site.urls)),
    #url(r'^admin/?$', 'django_cas.views.login', kwargs={'next_page': '/djadmin/'}),
    #(r'^djadmin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

