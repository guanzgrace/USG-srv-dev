import re
from functools import wraps
from django.conf import settings as conf
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.gzip import gzip_page
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django import forms
import json
import traceback
from utils.dsml import gdi
from models import *

def get_user(username):
    # Check if user can be here
    try:
        user = User.objects.get(netid=username)
    except:
        info = gdi(username)
        user = User(netid=username, firstname=info.get('givenName'),
                    lastname=info.get('sn'), pustatus=info.get('pustatus'))
        if info.get('puclassyear'):
            user.puclassyear = int(info.get('puclassyear'))
        if user.pustatus == 'undergraduate':
            user.save()
            # Create queues for each draw
            for draw in Draw.objects.all():
                queue = Queue.make(draw=draw, user=user)
                queue.save()
                user.queues.add(queue)
        else:
            return None
    return user

def check_user(fn):
    """Decorator for authenticating undergrads and handling first visits."""
    @wraps(fn)
    def fn_wrapper(request, *args, **kwargs):
        """Redirect to welcome if not seen, add Rooms user to request."""
        user = get_user(request.user.username)
        if not user:
            return HttpResponseForbidden()
        if not user.seen_welcome:
            return HttpResponseRedirect('/about/')
        request.rooms_user = user
        return fn(request, *args, **kwargs)

    return login_required(fn_wrapper)

@check_user
@cache_control(max_age=24*60*60, must_revalidate=True)
@cache_page(24*60*60)
@gzip_page
def index(request):
    draw_list = Draw.objects.order_by('id')
    mapscript = mapdata()
    drawscript = drawdata()
    response = render_to_response('rooms/base_dataPanel.html', locals())
    return response

@check_user
# May need to change if put in availability.
@cache_control(max_age=24*60*60, must_revalidate=True)
@cache_page(24*60*60)
@gzip_page
def draw(request, drawid):
    room_list = Room.objects.filter(building__draw__id=drawid)
    response = render_to_response('rooms/drawtab.html', locals())
    return response

def mapdata():
    buildings = Building.objects.order_by('id')
    maplist = []
    for building in buildings:
        draws = []
        for draw in building.draw.all():
            draws.append(draw.id)
        maplist.append({'name':building.name, 'draws':draws,
                        'lat':building.lat, 'lon':building.lon})
    mapstring = json.dumps(maplist)
    # Strip off port if present.
    domain = re.sub(r':[0-9]+$', '', conf.SITE_DOMAIN)
    real_time_addr = domain + ':' + conf.REAL_TIME_PORT
    mapstring = mapstring + ('; REAL_TIME_ADDR = "%s"' % real_time_addr)
    mapscript = '<script type="text/javascript">mapdata = %s</script>' % mapstring
    return mapscript

def drawdata():
    draws = Draw.objects.order_by('id')
    drawlist = []
    for draw in draws:
        drawlist.append({'name':draw.name, 'id':draw.id})
    drawstring = json.dumps(drawlist)
    drawscript = '<script type="text/javascript">drawdata = %s</script>' % drawstring
    return drawscript

def occlonghelper(room):
    occlong = 'Single'
    if room.occ == 1:
        occlong = 'Single'
    elif room.occ == 2:
        occlong = 'Double'
    elif room.occ == 3:
        occlong = 'Triple'
    elif room.occ == 4:
        occlong = 'Quad'
    else:
        occlong = 'Suite' + ' (' + str(room.occ) + ')'
    return occlong
    
def floorwordhelper(floor):
	
	if floor == 0:
		floorword = 'Ground'
	elif floor == 1:
		floorword = 'First'
	elif floor == 2:
		floorword = 'Second'
	elif floor == 3:
		floorword = 'Third'
	elif floor == 4:
		floorword = 'Fourth'
	elif floor == 5:
		floorword = 'Fifth'
	else:
		floorword = 'Zebra'
	return floorword;

@check_user
def bad_room(request):
    return HttpResponse("We are missing information for that room.")

# Single room view function
@check_user
def get_room(request, roomid):
    room = get_object_or_404(Room, pk=roomid)
    occlong = occlonghelper(room)
    floorword = floorwordhelper(room.floor)
    
    # Gather reviews for this room
    revs = Review.objects.filter(room=room)
    print 'num reviews found: %d' % (len(revs))
    
    pastReview = None
    try:
        pastReview = Review.objects.get(room=room, user=request.rooms_user)    #the review that the user has posted already (if it exists)
    except Review.DoesNotExist:
        pass
        
    if request.method == 'POST':
        review = request.POST.get('review', None)
        submit = request.POST.get('submit', None)
        delete = request.POST.get('delete', None)
        
        # user wants to review - clicked "Review this Room"
        if review:
            if pastReview:
                form = ReviewForm(instance=pastReview)
                return render_to_response('rooms/room_view.html', {'room' : room, 'occlong':occlong, 'floorword':floorword, 'reviews':revs, 'form': form, 'edit': True}, context_instance=RequestContext(request))
            else:   
                form = ReviewForm()
                return render_to_response('rooms/room_view.html', {'room' : room, 'occlong':occlong, 'floorword':floorword, 'reviews':revs, 'form': form}, context_instance=RequestContext(request))
        # user submitted the review
        elif submit:
            if pastReview:
                form = ReviewForm(request.POST, instance=pastReview)
            else:
                form = ReviewForm(request.POST)
                
            if form.is_valid():
                print 'ok valid'
                rev = form.save(commit=False)
                rev.user = request.rooms_user
                rev.room = room
                rev.save()
                revs = Review.objects.filter(room=room)
                print 'num reviews found: %d' % (len(revs))
                return render_to_response('rooms/room_view.html', {'room':room, 'occlong':occlong, 'floorword':floorword, 'reviews':revs})
            else:
                form = ReviewForm()
                return render_to_response('rooms/room_view.html', {'room':room, 'occlong':occlong, 'floorword':floorword, 'reviews':revs, 'form': form, 'error': 'Invalid submit data'})
        # user clicked "Delete this Review"
        elif delete:
            if pastReview:
                pastReview.delete()
                revs = Review.objects.filter(room=room)
                print 'num reviews found: %d' % (len(revs))
                return render_to_response('rooms/room_view.html', {'room':room, 'occlong':occlong, 'floorword':floorword, 'reviews':revs})
    
    return render_to_response('rooms/room_view.html', {'room':room, 'occlong':occlong, 'floorword':floorword, 'reviews':revs})
    
@check_user
def create_queue(request, drawid):
    draw = Draw.objects.get(pk=drawid)
    # Check if user already has queue for this draw
    if user.queues.filter(draw=draw):
        return HttpResponse("fail")
    queue = Queue.make(draw=draw, user=request.rooms_user)
    queue.save()
    request.rooms_user.queues.add(queue)
    return HttpResponse("pass")

# Send a queue invite
@check_user
def invite_queue(request):
    user = request.rooms_user
    try:
        draws = Draw.objects.all()
        netid = request.POST['netid']
        invited_draws = []
        for draw in draws:
            if int(request.POST['draw%d' % draw.id]):
                invited_draws.append(draw)
    except:
        return HttpResponse('Oops! Your form data is invalid. Try again!')

    receiver = get_user(netid)
    if not receiver:
        return manage_queues_helper(request, 'Sorry, the netid "%s" is invalid. Try again!' % netid)

    if len(invited_draws) == 0:
        return manage_queues_helper(request, 'You didn\'t select any draws. Try again!')

    for draw in invited_draws:
        invite = QueueInvite(sender=user, receiver=receiver, draw=draw,
                             timestamp=int(time.time()))
        invite.save();

    sender_name = "%s %s (%s@princeton.edu)" % (user.firstname, user.lastname, user.netid)
    url = conf.SITE_DOMAIN + "/manage_queues.html#received"
    subject = "Rooms: Queue Invitation"
    message = """Your friend %s invited you to share a room draw queue on the
Princeton Room Draw Guide! Accept the request at the following URL: 

%s""" % (sender_name, url)
    notify(receiver, subject, message)

    return render_to_response('rooms/invite_queue.html')

# Respond to a queue invite
@check_user
def respond_queue(request):
    user = request.rooms_user
    try:
        invite_id = int(request.POST['invite_id'])
        accepted = int(request.POST['accepted'])
    except:
        return HttpResponseForbidden()
    try:
        invite = user.q_received_set.get(pk=invite_id)
    except Exception as e:
        return HttpResponse(e)
    try:
        if accepted:
            queue = invite.accept()
            if not queue:
                return manage_queues_helper(request)
            friends = queue.user_set.all()
            for friend in friends:
                if user != friend:
                    receiver_name = "%s %s (%s@princeton.edu)" % (user.firstname, user.lastname, user.netid)
                    subject = "Rooms: %s Joined Your Queue" % user.firstname
                    url = "http://rooms.tigerapps.org/"
                    message = """Your friend %s has joined your room draw queue! Visit %s to browse rooms
to add. """ % (receiver_name, url)
                    notify(friend, subject, message)
        else:
            invite.deny()
    except Exception as e:
        return HttpResponse(e)


    return manage_queues_helper(request)

# Leave a queue that was previously shared
@check_user
def leave_queue(request):
    user = request.rooms_user
    try:
        draw = Draw.objects.get(pk=int(request.POST['draw_id']))
    except:
        return HttpResponse('')
    q1 = user.queues.get(draw=draw)
    if 1 == q1.user_set.count():
        return HttpResponse('')
    q2 = Queue.make(draw=draw, user=user)
    q2.save()
    qtrs = q1.queuetoroom_set.all()
    for qtr in qtrs:
        qtr.pk = None
        qtr.queue = q2
        qtr.save()
    user.queues.remove(q1)
    user.queues.add(q2)
    return manage_queues_helper(request);

@check_user
def settings(request):
    user = request.rooms_user
    if request.method == 'POST':
        if request.POST['form_type'] == 'settings':
            handle_settings_form(request, user)
            return render_to_response('rooms/user_settings.html', {'user': user, 'submitted': True})

    return render_to_response('rooms/user_settings.html', {'user': user})

def handle_settings_form(request, user):
    
    
    if(request.POST['phone']):
        phone = int(request.POST['phone'])
    
        if (not user.phone) or (phone != int(user.phone)):
            # Send confirmation code
            carriers = Carrier.objects.order_by('name')
    
            for carrier in carriers:
                code = (phone / 10000) * 3 + user.id + carrier.id * 7
                content = "Your confirmation code is: %s" % code
                send_mail("", content, 'rooms@tigerapps.org',
                      ["%s@%s" % (phone, carrier.address)], fail_silently=False)
                user.confirmed = False

    user.phone = request.POST['phone']
    user.do_text = bool(('do_text' in request.POST) and request.POST['do_text'])
    user.do_email = bool(('do_email' in request.POST) and request.POST['do_email'])
    user.save()


def handle_confirmphone_form(confirmation, user):
    if not user.phone:
        return False

    carrier_id = int(confirmation) - (int(user.phone) / 10000 * 3) - user.id;

    if carrier_id < 0 or carrier_id % 7 != 0:
        return False

    carrier_id /= 7

    try:
        carrier = Carrier.objects.get(id=carrier_id)
        user.carrier = carrier
        user.confirmed = True
        user.save()
        return True
    except:
        return False

 
@check_user
def confirm_phone(request):
    user = request.rooms_user
    if request.method == 'POST':
        if request.POST['form_type'] == 'settings':
            handle_settings_form(request, user)
            first_try = True
        elif request.POST['form_type'] == 'confirmphone':
            handle_confirmphone_form(request.POST['confirmation'], user)
            first_try = False
        else:
            first_try = True
    else:
        first_try = True

    return render_to_response('rooms/confirm_phone.html', {'user': user, 'first_try':first_try})

@check_user
def manage_queues(request, error=""):
    return manage_queues_helper(request, error)

def manage_queues_helper(request, error=""):
    user = request.rooms_user
    received_invites = QueueInvite.objects.filter(receiver=user)
    sent_invites = QueueInvite.objects.filter(sender=user)
    user_queues = user.queues.all()
    shared_queues = []
    for q in user_queues:
        if q.user_set.count() > 1:
            shared_queues.append(q)
    return render_to_response('rooms/manage_queues.html', {'user' : user,
                                                           'draws' : Draw.objects.all(),
                                                           'received_invites' : received_invites,
                                                           'sent_invites' : sent_invites,
                                                           'shared_queues' : shared_queues,
                                                           'error' : error })

@login_required
def about(request):
    user = get_user(request.user.username)
    if user:
        user.seen_welcome = True
        user.save()
    return render_to_response('rooms/about.html')

#helper function
def notify(user, subject, message):
    if user.do_email:
        send_mail(subject, message, 'rooms@tigerapps.org',
                      ["%s@princeton.edu" % user.netid], fail_silently=False)
    if user.do_text and user.confirmed:
        send_mail(subject, message, 'rooms@tigerapps.org',
                      ["%s@%s" % (user.phone, user.carrier.address)], fail_silently=False)



