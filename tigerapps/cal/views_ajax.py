################################################################
# Project: Princeton Events Calendar
# Authors: Ethan Goldstein, Samantha Hantman, Dana Hoffman, 
#		   Adriana Susnea, and Michael Yaroshefsky 
# Date:    May 11, 2010
################################################################
# Title:  views_ajax.py
# Info :  called by AJAX on pages
################################################################

from django.http import *
from django.db.models import Count
from models import *
from utils.dsml import namelookup
import json

def get_all_tags(request):
    tags = [tag.category_name for tag in EventCategory.objects.all()]
    return HttpResponse(json.dumps(tags), content_type="application/json")

def get_all_graphsearch(request):
    """
    Returns json list of rels:
        entry type (all, tags, feats, creators)
        entry id (in database)
        entry image
    of search:
        entry search name
        count of clusters matching entry
    THIS SHOULD BE CACHED
    """
        
    rels = [(0, 0)]
    search = [('all', 99999999)]

    #TODO: use ids instead of names in tag/crceator
    tags = EventCategory.objects.all().annotate(c=Count('tag_clusters'))
    rels += [(1, tag.category_name) for tag in tags]
    search += [(tag.category_name, tag.c) for tag in tags]

    feats = EventFeature.objects.all().annotate(c=Count('feature_clusters'))
    rels += [(2, feat.id, feat.feature_icon) for feat in feats]
    search += [(feat.feature_name.lower(), feat.c) for feat in feats]

    creators = CalUser.objects.all().annotate(c=Count('creator_clusters'))
    rels = [(3, u.user_netid) for u in creators]
    search += [(u.user_netid.lower(), u.c) for u in creators]

    data = {
        'rels': rels,
        'search': search,
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


def netidlookup(request):
	""" Return a formatted HTML chunk of the names found using the DSML for the query """
	lookup =  namelookup(request.POST['netid'])
	html = '<div id="invite_results"><h4>Search Results</h4>'
	if lookup:
		html = html + '<ul>'
		for result in lookup:
			if 'mail' in result and 'uid' in result and 'displayName' in result:
				html = html	+ '<li><a href="#" onClick="$(\'#invitee\').val(\''+result['uid']+'\'); document.invitation.submit();">' + result['displayName'] + ' (' + result['uid']+ ')</a></li>'
			elif 'mail' in result and 'uid' in result:
				html = html	+ '<li><a href="#" onClick="$(\'#invitee\').val(\''+result['uid']+'\'); document.invitation.submit();">' + result['mail'] + ' (' + result['uid']+ ')</a></li>'
		
		html = html + '</ul>'
		html = html + '<p>Click a name to select as recipient.</p></div>'
	else:
		html = html + '<p>No results found.</p></div>'
		
	return HttpResponse(html)
	
def allguests(request):
	""" Return an HTML chunk with all names of event attendees """
	eventid = request.POST['eventid']
	try:
		event = Event.objects.get(pk = eventid)
	except:
		return
	html = '<ol>'
	attendees = RSVP.objects.filter(rsvp_event = event, rsvp_type = 'Accepted', rsvp_user__user_privacy_enabled = False).order_by('rsvp_user__user_netid')

	for rsvp in attendees:
		html = html + "<li>%s</li>" % (rsvp.rsvp_user.full_name_suffix())

	private = RSVP.objects.filter(rsvp_event = event, rsvp_type = 'Accepted', rsvp_user__user_privacy_enabled = True).count()
	if private:
		html = html + '<li class="extra">%s private guest%s</li>' % (private,('s' if private != 1 else ''))

	html = html + '</ol>'

	return HttpResponse(html)
