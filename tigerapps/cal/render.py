################################################################
# Project: Princeton Events Calendar
# Authors: Ethan Goldstein, Samantha Hantman, Dana Hoffman, 
#           Adriana Susnea, and Michael Yaroshefsky 
# Date:    May 11, 2010
################################################################
# Title:  render.py
# Info :  'intercept' a call to render, and do some common things
################################################################

from django import shortcuts
from datetime import datetime
from models import *
from usermsg import MsgMgr, Msg
from globalsettings import our_site
from cal.cauth import current_user
from cal import query


def render_to_response(request, template, out_dict):
    """
    Load context with common parts of each page. Includes:
    - User data for top bar
    - Hot/new events for bottom spotlight
    """
    user = current_user(request)
    if user:
        out_dict['user_data'] = user
        # Top menu
        out_dict['my_invites'] = query.rsvps_pending(user)
        out_dict['unread_msgs'] = UserMessage.objects.filter(um_user=user, um_date_read=None)
        # Bottom spotlight
        out_dict['my_viewed'] = query.events_myviewed(user, limit=3, group=False)
    
    # ???
    out_dict['v_messages'] = MsgMgr.iterable(request)

    # Bottom spotlight
    out_dict['hot_events'] = query.events_hot(limit=3, group=False)
    out_dict['new_events'] = query.events_new(limit=3, group=False)
    
    #out_dict['our_site'] = our_site
    #Msg('This site will be undergoing planned maintenance tonight. Sorry for any inconvenience.',1).push(request)
    return shortcuts.render_to_response(template, out_dict)



def prepare_user_rightcol(user, out_dict):
    """
    For cal/modules/user_rightcol.html, which isn't being used right now
    """
    out_dict['user_rc_accepted'] = query.rsvps_accepted(user, 3)
    out_dict['user_rc_pending'] = query.rsvps_pending(user, 3)


def go_back(request, error_msg=None, type=0):
    if error_msg:
        Msg(error_msg,type).push(request)
    ref = request.META.get('HTTP_REFERER',None)
    if ref and ref.find(our_site) == 0:
        ref = ref.replace(our_site,'/',1)
    else:
        ref = '/'
    return HttpResponseRedirect(ref)

