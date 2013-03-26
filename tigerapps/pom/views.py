import datetime, json, cgi
from collections import defaultdict
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.template import RequestContext
from django.core.cache import cache
from django.core.mail import send_mail

from utils.srvlog import log
from pom import cal_event_query
from pom.bldg_info import *
from pom.campus_map_codes import campus_codes
from pom.campus_map_bldgs_info import campus_info
from pom.scrape import menus, printers, laundry



# not used due to direct_to_template in urls.py
def index(request, offset):
    return render_to_response('pom/index.html', {}, RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_staff)
def refresh_cache(request):
    cache.set('pom.menus', (datetime.datetime.now(), menus.scrape_all()))
    cache.set('pom.printers', (datetime.datetime.now(), printers.scrape_all()))
    cache.set('pom.laundry', (datetime.datetime.now(), laundry.scrape_all()))
    return HttpResponse('success')


def get_bldg_names_json(request):
    '''
    make dictionary of name, code pairs for use in location-based filtering
    '''
    bldg_names = dict((name[0], code) for code, name in BLDG_INFO.iteritems())
    response_json = json.dumps(bldg_names)
    return HttpResponse(response_json, content_type="application/javascript")

def get_cal_events_json(request, events_list=None):
    if not events_list:
        events_list = filter_cal_events(request)
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
        half_hrs_delta = int(round(delta.total_seconds()/1800)) % 48
        time_index = str(delta.days) + '-' + str(half_hrs_delta)
        
        events_data[event.event_id] = {'bldgCode': event.event_location,
                                       'tooltip': '<span class="tipsy-bold">%s-%s</span>: %s'%(event.time_start_str, event.time_end_str, cgi.escape(event.event_cluster.cluster_title))}
        mark_data[time_index].append(event.event_id)
        
    return {'eventsData': events_data, 'markData': mark_data}



def bldgs_for_filter(request):
    '''
    Return a JSON-list of building codes that should be highlighted given
    the filters in the GET parameters of the request.
    '''
    if 'type' not in request.GET:
        return HttpResponseServerError("No type in GET")
    filter_type = request.GET['type']

    if filter_type == '0': #standard event
        events = filter_cal_events(request)
        bldgsList = list(set((event.event_location for event in events)))
        
    elif filter_type == '2': #menus
        bldgsList = getBldgsWithMenus()
    
    elif filter_type == '3': #laundry
        bldgsList = getBldgsWithLaundry()
    
    elif filter_type == '4': #printers
        bldgsList = getBldgsWithPrinters()
        
    else:
        return HttpResponseServerError("Bad filter type in GET request: %s" % filter_type)
        
    response_json = json.dumps({'error': None,
                                      'bldgs': tuple(bldgsList)})
    return HttpResponse(response_json, content_type="application/javascript")




def data_for_bldg(request, bldg_code):
    '''
    Return the HTML that should be rendered in the info box given the
    building in the GET parameter of the request
    '''
    if 'type' not in request.GET:
        return HttpResponseServerError("No type in GET")
    filter_type = request.GET['type']
    
    try:
        if filter_type == '0': #standard event
            events = filter_cal_events(request, bldg_code)
            html = render_to_string('pom/event_info.html',
                                    {'bldg_name': BLDG_INFO[bldg_code][0],
                                     'events': events})
            response_dict = dict({'error': None, 'html': html, 'bldgCode': bldg_code}.items() + get_cal_events_json(request, events).items())
        
        elif filter_type == '2': #menus        
            #assert building is a dining hall
            if bldg_code not in getBldgsWithMenus():
                err = 'requested menu info from invalid building ' + BLDG_INFO[bldg_code][0]
                response_dict = {'error': err}
            else:
                menu_list, timestamp = cache.get('pom.menus')
                menu_list = list(set([(hall, menu) for hall, menu in menu_list.items()]))
                menu_list = sorted(menu_list, key = lambda x: x[0])
                for tup in menu_list:
                    tup[1].meals = [(name, meal) for name, meal in tup[1].meals.items()]
                    tup[1].meals = sorted(tup[1].meals, key = lambda x: menus_sorter(x[0]))
                menu = dict(menu_list)[bldg_code]
                html = render_to_string('pom/menu_info.html',
                                        {'bldg_name': BLDG_INFO[bldg_code][0],
                                         'menu': menu,
                                         'timestamp': timestamp})
                response_dict = {'error': None, 'html': html, 'bldgCode': bldg_code}
    
        elif filter_type == '3': #laundry
            #assert building contains laundry room
            if bldg_code not in getBldgsWithLaundry():
                err = 'requested laundry info from invalid building ' + BLDG_INFO[bldg_code][0]
                response_dict = {'error': err}
            else:
                machine_mapping, timestamp = cache.get('pom.laundry')
                machine_list_bldg = machine_mapping[bldg_code]
                html = render_to_string('pom/laundry_info.html',
                                        {'bldg_name': BLDG_INFO[bldg_code][0],
                                         'machine_list' : machine_list_bldg,
                                         'timestamp': timestamp})
                response_dict = {'error': None, 'html': html, 'bldgCode': bldg_code}
    
        elif filter_type == '4': #printers
            #assert building contains printer
            if bldg_code not in getBldgsWithPrinters():
                err = 'requested printer info from invalid building ' + BLDG_INFO[bldg_code][0]
                response_dict = {'error': err}
            else:
                printer_mapping, timestamp = cache.get('pom.printers')
                printer_list = [printer for printer in printer_mapping[bldg_code]]
                printer_list = sorted(printer_list, key=lambda printer: printer.loc)
    
                html = render_to_string('pom/printer_info.html',
                                        {'bldg_name': BLDG_INFO[bldg_code][0],
                                         'printers' : printer_list,
                                         'timestamp': timestamp})
                response_dict = {'error': None, 'html': html, 'bldgCode': bldg_code}
    
        elif filter_type == '5': #location
            codes = campus_codes[bldg_code]
            if codes[0] == 0:
                info = None
            else:
                info = [campus_info[code] for code in codes]
            html = render_to_string('pom/location_info.html',
                                    {'bldg_name':BLDG_INFO[bldg_code][0],
                                     'info':info})
            response_dict = {'error': None, 'html': html, 'bldgCode': bldg_code}
        
        else:
            return HttpResponseServerError("Bad filter type in GET request: %s" % filter_type)

    except Exception, e:
        response_dict = {'error': str(e)}
        
    
    response_json = json.dumps(response_dict)
    return HttpResponse(response_json, content_type="application/javascript")



def data_for_all(request):
    '''
    Return the HTML that should be rendered in the info box given the
    building in the GET parameter of the request
    '''
    if 'type' not in request.GET:
        return HttpResponseServerError("No type in GET")
    filter_type = request.GET['type']
    
    
    try:
        if filter_type == '0': #standard event
            events = filter_cal_events(request)
            html = render_to_string('pom/event_info.html',
                                    {'all_events': True, 
                                     'events': events})
            response_json = json.dumps(dict({'error': None, 'html': html}.items() + get_cal_events_json(request, events).items()))
            
        elif filter_type == '2': #menus
            menu_list, timestamp = cache.get('pom.menus')
            menu_list = list(set([(hall, menu) for hall, menu in menu_list.items()]))
            menu_list = sorted(menu_list, key = lambda x: x[0])
            for tup in menu_list:
                tup[1].meals = [(name, meal) for name, meal in tup[1].meals.items()]
                tup[1].meals = sorted(tup[1].meals, key = lambda x: menus_sorter(x[0]))
            html = render_to_string('pom/menu_info_all.html',
                                    {'menu_list': menu_list,
                                     'bldg_info': BLDG_INFO,
                                     'timestamp': timestamp})
            response_json = json.dumps({'error': None,
                                              'html': html})
   
        elif filter_type == '3': #laundry
            machine_mapping, timestamp = cache.get('pom.laundry')
            machine_list = [x for k,v in machine_mapping.iteritems() for x in v]
            machine_list = sorted(machine_list, key=lambda x: x[0])
            html = render_to_string('pom/laundry_info.html',
                                    {'bldg_name': 'All Laundry Machines',
                                     'machine_list' : machine_list,
                                     'timestamp': timestamp})
            response_json = json.dumps({'error': None,
                                              'html': html})

        elif filter_type == '4': #printers
            printer_mapping, timestamp = cache.get('pom.printers')
            printer_list = [printer for bldg_code,printers_bldg in printer_mapping.items() for printer in printers_bldg]
            printer_list = sorted(printer_list, key=lambda printer: printer.loc)
            html = render_to_string('pom/printer_info.html',
                                    {'bldg_name': "All Printers",
                                     'printers' : printer_list,
                                     'timestamp': timestamp})
            response_json = json.dumps({'error': None,
                                              'html': html})
        
        else:
            return HttpResponseServerError("Bad filter type in GET request: %s" % filter_type)

    except Exception, e:
        response_json = json.dumps({'error': str(e)})
        
    return HttpResponse(response_json, content_type="application/javascript")



####
#Helper functions for views above
####

def filter_cal_events(request, bldg_code=None):
    events = []
    try:
        if bldg_code: #Filter by bldg
            events = cal_event_query.filter_by_bldg(events, bldg_code)
            if not events: return events
        if request.GET['search']: #Filter by search term
            events = cal_event_query.filter_by_search(events, request.GET['search'])
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

    for event in events:
        desc = event.event_cluster.cluster_description
        event.short_desc = desc[:100]
        event.long_desc = desc[100:]
        if (not bldg_code) and event.event_location in BLDG_INFO:
            event.event_location_name = BLDG_INFO[event.event_location][0]
        if event.event_location_details.isdigit():
            event.event_location_details = 'Room ' + event.event_location_details
        event.time_start_str = event.event_date_time_start.strftime('%I:%M%p').lstrip('0').lower()
        event.time_end_str = event.event_date_time_end.strftime('%I:%M%p').lstrip('0').lower()
    return events
     

MENUS_ORDER = {'Breakfast':0, 'Brunch':1, 'Lunch':2, 'Dinner':3}
def menus_sorter(name):
    if name in MENUS_ORDER:
        return MENUS_ORDER[name]
    else:
        return 4


