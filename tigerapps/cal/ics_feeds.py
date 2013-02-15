################################################################
# Project: Princeton Events Calendar
# Authors: Ethan Goldstein, Samantha Hantman, Dana Hoffman, 
#		   Adriana Susnea, and Michael Yaroshefsky 
# Date:    May 11, 2010
################################################################
# Title:  views_events.py
# Info :  rendering pages and executing actions related to events
################################################################

from globalsettings import *
import sys, os
sys.path.append(os.path.expanduser('%s/' % site_root))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 

from django.http import *

import urllib, re
from datetime import datetime, timedelta
from app.models import *

from icalendar import Calendar as VCALENDAR
from icalendar import Event as VEVENT
from icalendar.prop import vDDDTypes

webcal = WebcalSubscription(
	webcal_url = 'http://www.google.com/calendar/ical/princetonusg.com_0jbjnnqm6d7tipveh3aerr6p8c%40group.calendar.google.com/public/basic.ics',
	webcal_title = 'Academic Calendar',
	webcal_description = 'List of events for the academic calendar',
	webcal_default_location = 'Princeton University',
	webcal_default_category = EventCategory.objects.get(category_name='Other'),
	webcal_user_added = CalUser.objects.get(user_netid='yaro')
	)
webcal.save()

webcal2 = WebcalSubscription(
	webcal_url = ' http://www.google.com/calendar/ical/cloister%40princeton.edu/public/basic.ics',
	webcal_title = 'Cloister Calendar',
	webcal_description = 'List of events for cloister',
	webcal_default_location = 'Cloister',
	webcal_default_category = EventCategory.objects.get(category_name='Other'),
	webcal_user_added = CalUser.objects.get(user_netid='yaro')
	)
webcal2.save()


def AddOrUpdateWebcal(webcal):
	calString = urllib.urlopen(webcal.webcal_url).read()
	cal = VCALENDAR.from_string(calString)
	eventCluster = EventCluster(
			cluster_title = webcal.webcal_title,
			cluster_description = webcal.webcal_description,
			cluster_user_created = webcal.webcal_user_added,
			cluster_rsvp_enabled = False,
			cluster_board_enabled = True,
			cluster_notify_boardpost = False,
		)
    eventCluster.cluster_tags.add(webcal.webcal_default_category)
	eventCluster.save()
	
	for component in cal.walk():
		if(component.name == 'VEVENT'):
			valid = True
			proplist = {}
			REQ_PROPS = ('UID','SUMMARY','DTSTART','DTEND')
			for prop in component.property_items():
				proplist[prop[0]] = prop[1]

			for rprop in REQ_PROPS:
				if rprop not in proplist:
					print 'MISSING %s' % rprop
					valid = False

			if valid:
				try:
					updateEvent = Event.objects.get(event_webcal_uid = proplist['UID'])
					print 'I found my old friend, %s' % proplist['UID']
				except:
					dtstart = vDDDTypes.from_ical(proplist['DTSTART'].ical())
					dtend = vDDDTypes.from_ical(proplist['DTEND'].ical())
					add_event = Event(
						event_webcal_uid = proplist['UID'],
						event_user_last_modified = CalUser.objects.get(user_netid='yaro'),
						event_subtitle = proplist['SUMMARY'],
						event_subdescription = proplist.get('DESCRIPTION','No description provided.'),
						event_date_time_start = dtstart,
						event_date_time_end = dtend,
						event_location_details = proplist.get('LOCATION',''),
						event_cluster = eventCluster,
						event_cancelled = False,
						event_attendee_count = 0,)
					add_event.save()

AddOrUpdateWebcal(webcal);
