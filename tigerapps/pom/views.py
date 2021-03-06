from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.template import RequestContext
from django.core.cache import cache
import datetime, json, cgi
from collections import defaultdict

from pom import cal_event_query
from pom.bldg_info import *
from pom.campus_map_codes import campus_codes
from pom.campus_map_bldgs_info import campus_info
from pom.scrape import menus, printers, laundry
import settings



####
# User-facing
####

# not used due to direct_to_template in urls.py
def index(request, offset):
    return render_to_response('pom/index.html', {}, RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def refresh_cache(request):
    # causes internal server error because HTTP request takes too long. need to
    # replace with something that makes async caching call instead
    #cache.set('pom.menus', (datetime.datetime.now(), menus.scrape_all()))
    #cache.set('pom.printers', (datetime.datetime.now(), printers.scrape_all()))
    #cache.set('pom.laundry', (datetime.datetime.now(), laundry.scrape_all()))
    #return HttpResponse('success')
    return HttpResponse('feature currently disabled')




####
# For setting up any widgets used by the map
####

KWAC = {
    0: 'Events matching',
    2: 'Menus at',
    4: 'Printers at',
    5: 'Locations matching',
}
def widget_search_resp(request):
    term = request.GET['term']
    terms = term.split()
    KWAC_terms = [v.split() for v in KWAC.values()]

    for (layer, v) in KWAC.iteritems():
        pass

    response_json = json.dumps(matches)
    return HttpResponse(response_json, content_type="application/javascript")


def widget_locations_setup(request):
    '''
    Return json dictionary of name, code pairs for use in location-based
    filtering
    '''
    response_json = cache.get('pom.locations_setup')
    if response_json is None:
        bldg_names = []
        already = set()
        for code,nums in campus_codes.iteritems():
            for num in nums:
                if num != 0:
                    name = campus_info[num]['name']
                    if name not in already:
                        bldg_names.append({
                            'value': name,
                            'label': name,
                            'code': code,
                            'order': 1
                        })
                        already.add(name)
        for code,nums in campus_codes.iteritems():
            for num in nums:
                if num != 0:
                    for org in campus_info[num]['organizations']:
                        name = org['name']
                        if name not in already:
                            bldg_names.append({
                                'value': name,
                                'label': name,
                                'code': code,
                                'order': 2
                            })
                            already.add(name)
        bldg_names = sorted(bldg_names, key=lambda x: (x['order'], x['label']))
        response_json = json.dumps(bldg_names)
        cache.set('pom.locations_setup', response_json)
    return HttpResponse(response_json, content_type="application/javascript")




####
# Directly called when a filter or layer is clicked
####

SCRAPE_LAYERS = {
    '2': ('menus', menus),
    '3': ('laundry', laundry),
    '4': ('printers', printers)
}

def get_filtered_bldgs(request):
    '''
    Return a JSON-list of building codes that should be highlighted given
    the filters in the GET parameters of the request.
    '''
    if 'type' not in request.GET:
        return HttpResponseServerError("No type in GET")
    layer = request.GET['type']
    rid = request.GET['rid']

    if layer == '0': #event
        events = filter_events(request)
        bldgsList = list(set((event.event_location for event in events)))
        
    elif layer in SCRAPE_LAYERS:
        bldgsList = SCRAPE_LAYERS[layer][1].get_bldgs()
        
    else:
        return HttpResponseServerError("Bad layer in GET request: %s" % layer)
        
    response_json = json.dumps({'bldgs': tuple(bldgsList), 'rid': rid})
    return HttpResponse(response_json, content_type="application/javascript")


def get_filtered_data_bldg(request, bldg_code):
    '''
    Return the HTML that should be rendered in the info box given the
    building in the GET parameter of the request
    '''
    if 'type' not in request.GET:
        return HttpResponseServerError("No type in GET")
    layer = request.GET['type']
    rid = request.GET['rid']
    
    try:
        if layer == '0': #event
            events = filter_events(request, bldg_code)
            html = render_to_string('pom/data_events.html',
                                    {'bldg_name': BLDG_INFO[bldg_code][0],
                                     'events': events})
            rendered = build_events_data(request, events)
            rendered['html'] = html
            rendered['bldgCode'] = bldg_code
        
        elif layer == '5': #location
            codes = campus_codes[bldg_code]
            if codes[0] == 0:
                info = None
            else:
                info = [campus_info[code] for code in codes]
            html = render_to_string('pom/data_locations.html',
                                    {'bldg_name':BLDG_INFO[bldg_code][0],
                                     'info':info})
            rendered = {'html': html, 'bldgCode': bldg_code}
        
        else:
            return HttpResponseServerError("Bad filter type in GET request: %s" % layer)

    except Exception, e:
        return HttpResponseServerError("Uncaught exception: %s" % str(e))
        
    rendered['rid'] = rid
    response_json = json.dumps(rendered)
    return HttpResponse(response_json, content_type="application/javascript")


def get_filtered_data_all(request):
    '''
    Return the HTML that should be rendered in the info box given the
    building in the GET parameter of the request
    '''
    if 'type' not in request.GET:
        return HttpResponseServerError("No type in GET")
    layer = request.GET['type']
    rid = request.GET['rid']
    
    try:
        if layer == '0': #event
            events = filter_events(request)
            html = render_to_string('pom/data_events.html',
                                    {'all_events': True, 
                                     'events': events})
            rendered = build_events_data(request, events)
            rendered['html'] = html
            
        elif layer in SCRAPE_LAYERS:
            mod_name,mod = SCRAPE_LAYERS[layer]
            cache_key = 'pom.' + mod_name
            scraped = cache.get(cache_key)
            if scraped is not None:
                rendered = mod.render(scraped)
            else:
                html = render_to_string('pom/data_unavailable.html', {
                    'url_alt': mod.url_alt})
                rendered = {'html': render_to_string('pom/data_unavailable.html')}
   
        else:
            return HttpResponseServerError("Bad filter type in GET request: %s" % layer)

    except Exception, e:
        return HttpResponseServerError("Uncaught exception: %s" % str(e))
        
    rendered['rid'] = rid
    response_json = json.dumps(rendered)
    return HttpResponse(response_json, content_type="application/javascript")




####
# For filtering data for a layer
####

def filter_events(request, bldg_code=None):
    events = []
    try:
        if bldg_code: #Filter by bldg
            events = cal_event_query.filter_by_bldg(events, bldg_code)
            if not events: return events
        
        #Filter by time, must be last since it's hacky
        start_day = datetime.datetime(int(request.GET['y0']), int(request.GET['m0']), int(request.GET['d0']))
        end_day = start_day + datetime.timedelta(days=int(request.GET['nDays'])-1)
        events = cal_event_query.filter_by_day_hour(
            events, start_day, end_day,
            int(request.GET['h0']), int(request.GET['i0']),
            int(request.GET['h1']), int(request.GET['i1']))
    except Exception, e:
        return HttpResponseServerError('Bad GET request: '+ str(e))

    from sanitizer.templatetags.sanitizer import escape_html
    for event in events:
        desc = escape_html(event.event_cluster.cluster_description,
            allowed_tags=settings.SANITIZER_ALLOWED_TAGS,
            allowed_attributes=settings.SANITIZER_ALLOWED_ATTRIBUTES)
        # TODO: this way of splitting the description is vulnerable to bad HTML tags 
        # We don't want to cut open a tag in the middle, or to cut open a link tag
        # in the middle.  XXX I don't think the check for cutting open a link tag
        # in the middle works right.
        # TODO: this also doesn't deal with opened i's, b's, etc..
        split = 100
        opened = 0
        opened_a = False
        for i, c in enumerate(desc[:split]):
            if c == '<':
                opened += 1
                if not opened_a:
                    opened_a = (desc[i:i+2].lower() == '<a')
                else:
                    opened_a = (desc[i:i+3].lower() != '</a')
            elif c == '>':
                opened -= 1
        if opened == 1:
            for c in desc[split:]:
                split += 1
                if c == '>':
                    break
        if opened_a:
            for c in desc[split:]:
                split += 1
                if c == '<':
                    opened_a = (desc[i:i+3].lower() != '</a')
                elif c == '>':
                    if not opened_a:
                        break
        event.short_desc = desc[:split]
        event.long_desc = desc[split:]
        if (not bldg_code) and event.event_location in BLDG_INFO:
            event.event_location_name = BLDG_INFO[event.event_location][0]
        if event.event_location_details.isdigit():
            event.event_location_details = 'Room ' + event.event_location_details
        event.time_start_str = event.event_date_time_start.strftime('%I:%M%p').lstrip('0').lower()
        event.time_end_str = event.event_date_time_end.strftime('%I:%M%p').lstrip('0').lower()
    return events
     



####
# For building filtered data for a layer
####

def build_events_data(request, events_list=None):
    if not events_list:
       events_list = filter_events(request)
    try:
        start_date = datetime.datetime(int(request.GET['y0']), int(request.GET['m0']), int(request.GET['d0']))
        start_index = 2*int(request.GET['h0']) + round(int(request.GET['i0'])/30)
        end_index = 2*int(request.GET['h1']) + round(int(request.GET['i1'])/30)
        n_days = int(request.GET['nDays'])
    except Exception, e:
        return HttpResponseServerError('Bad GET request: missing get params (%s)' % str(e))
    
    events_data = {}
    mark_data = defaultdict(list)
    for event in events_list:
        e_start = event.event_date_time_start
        delta = e_start - start_date
        half_hrs_delta = int(delta.total_seconds()/1800) % 48
        time_index = str(delta.days) + '-' + str(half_hrs_delta)
        
        events_data[event.event_id] = {
            'bldgCode': event.event_location,
            'tooltip': '<span class="tipsy-bold">%s-%s</span>: %s' % (
                event.time_start_str,
                event.time_end_str,
                cgi.escape(event.event_cluster.cluster_title)),
        }
        mark_data[time_index].append(event.event_id)
        
    return {'eventsData': events_data, 'markData': mark_data}

