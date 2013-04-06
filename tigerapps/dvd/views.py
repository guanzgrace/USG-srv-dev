from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.template import RequestContext, loader
from django_cas.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from dvd.emails import *
from dvd.models import *
from utils.dsml import gdi
from dvd import permissions
import datetime
import dvd.emails as dvd_emails


def home(request):
    DVD_list = DVD.objects.all().order_by('sortname')
    blurb = Blurb.objects.get(title='homepage')
    return render_to_response('dvd/index.html', {'DVD_list': DVD_list, 'blurb_homepage': blurb.content}, RequestContext(request))
    
@login_required
def notify(request, dvd_id):
    dvd = DVD.objects.get(dvd_id=dvd_id)
    try:
        notice = Notice.objects.filter(netid=request.user.username).get(dvd=dvd)
        title = "Ruh-roh!"
        confirm = "You're already going to be notified when a copy of " + dvd.name + " comes by. Hold your horses!"
    except Notice.DoesNotExist:
        notice = Notice(netid=request.user.username, dvd=dvd)
        notice.save()
        title = "Success!"
        confirm = "You will get an email as soon as a copy of " + dvd.name + " is available"
    return render_to_response('dvd/confirm.html', {'title': title, 'confirm': confirm}, RequestContext(request))


#####
# Admin views
#####

@login_required
@user_passes_test(lambda u: permissions.in_dvdadmin_group(u))
def admin(request):
    rentalList = Rental.objects.filter(dateReturned=None).order_by('dateDue').reverse()
    return render_to_response('dvd/dvdadmin.html', {'rentalList': rentalList}, RequestContext(request))


@login_required
@user_passes_test(lambda u: permissions.in_dvdadmin_group(u))
def checkout_1(request):
    return render_to_response('dvd/checkout_1.html', context_instance=RequestContext(request))
    
@login_required
@user_passes_test(lambda u: permissions.in_dvdadmin_group(u))
def checkout_2(request):
    if request.method == 'POST':
        netid = request.POST['netid']
        user_info = gdi(netid)
        if user_info is None:
            return render_to_response('dvd/user_not_found.html', context_instance=RequestContext(request))

        due = request.POST['due']
        checked_pks = request.POST.getlist('dvd')
        now = datetime.datetime.now()
        checked_list = []
        for pk in checked_pks:
            dvd = DVD.objects.get(dvd_id=int(pk))
            dvd.amountLeft -= 1
            dvd.save()
            rental = Rental(netid=netid, dvd=dvd, dateRented=now, dateDue=(now + datetime.timedelta(days=int(due))), dateReturned=None)
            rental.save()
            checked_list.append(dvd)
        return render_to_response('dvd/checkout_complete.html', {'netid': netid, 'checked_list': checked_list}, RequestContext(request))

    if 'netid' not in request.GET:
        return HttpResponseRedirect('/dvd/checkout/1/')
    netid = request.GET['netid']
    user_info = gdi(netid)
    if user_info is None:
        return render_to_response('dvd/user_not_found.html', context_instance=RequestContext(request))
        
    warningList = Rental.objects.filter(netid=netid).filter(dateReturned=None).order_by('dateDue')
    DVD_list = DVD.objects.all().exclude(amountLeft=0).order_by('name')
    return render_to_response('dvd/checkout_2.html', {'netid': netid, 'DVD_list': DVD_list, 'warningList': warningList}, RequestContext(request))


@login_required
@user_passes_test(lambda u: permissions.in_dvdadmin_group(u))
def checkin_user(request):
    if request.method == "POST":
        netid = request.POST['netid']
        rental_list = request.POST.getlist('rental') #list of dvd's checked
        checked_list = []
        for rental_id in rental_list:
            rental = Rental.objects.get(rentalID=rental_id, dateReturned=None, netid=netid)
            rental.dateReturned = datetime.datetime.now()
            rental.save()
            #checkin DVD
            checkin_dvd = rental.dvd
            checkin_dvd.amountLeft += 1
            checkin_dvd.save()
            checked_list.append(checkin_dvd)
            dvd_emails.email_if_available(checkin_dvd)
        return render_to_response('dvd/checkinuser_complete.html', {'checked_list': checked_list, 'netid': netid}, RequestContext(request))
    
    if 'netid' not in request.GET:
        return render_to_response('dvd/checkinuser_1.html', context_instance=RequestContext(request))
    netid = request.GET['netid']
    user_info = gdi(netid)
    if user_info is None:
        return render_to_response('dvd/user_not_found.html', context_instance=RequestContext(request))

    rentalList = Rental.objects.filter(netid=netid, dateReturned=None).order_by('dvd__sortname')
    return render_to_response('dvd/checkinuser_2.html', {'netid': netid, 'rentalList': rentalList}, RequestContext(request))



@login_required
@user_passes_test(lambda u: permissions.in_dvdadmin_group(u))
def checkin_dvd(request):
    if request.method == "POST":
        checked_list = []
        if "dvd" in request.POST:
            ambiguous_list = [] # When more than one copy is checked out
            dvd_list = request.POST.getlist('dvd') #list of dvd's checked
            for dvd_id in dvd_list:
                checkin_dvd = DVD.objects.get(pk=dvd_id)
                if checkin_dvd.amountTotal - checkin_dvd.amountLeft > 1:
                    #if there's copies of dvd_id still checked out
                    ambiguous_list.append((checkin_dvd, Rental.objects.filter(dateReturned=None, dvd=checkin_dvd)))
                else:
                    #if all of the copies of dvd_id are checked in
                    checked_list.append(checkin_dvd)
                    rental = Rental.objects.get(dateReturned=None, dvd=checkin_dvd)
                    rental.dateReturned = datetime.datetime.now()
                    rental.save()
                    #checkin DVD
                    checkin_dvd.amountLeft += 1
                    checkin_dvd.save()
                dvd_emails.email_if_available(checkin_dvd)
            if ambiguous_list:
                #This allows the person checking in the dvd to select which copy was checked in
                return render_to_response('dvd/ambiguous.html', {'ambiguous_list': ambiguous_list, 'checked_list': checked_list}, RequestContext(request))
        else:
            rental_list = [(k[4:],v) for k,v in request.POST.iteritems() if k.startswith('dvd-')]
            for dvd_id, rental_id in rental_list:
                checkin_dvd = DVD.objects.get(pk=dvd_id)
                checked_list.append(checkin_dvd)
                rental = Rental.objects.get(rentalID=rental_id)
                rental.dateReturned = datetime.datetime.now()
                rental.save()
                #checkin DVD
                checkin_dvd.amountLeft += 1
                checkin_dvd.save()
                dvd.emails.email_if_available(checkin_dvd)
        return render_to_response('dvd/checkindvd_complete.html', {'checked_list': checked_list}, RequestContext(request))

    dvd_list = DVD.objects.all()
    excludes = []
    for dvd in dvd_list:
        if dvd.amountLeft == dvd.amountTotal:
            excludes.append(dvd.pk)
    dvd_list = dvd_list.exclude(pk__in=excludes).order_by('sortname')
    return render_to_response('dvd/checkindvd_1.html', {'dvd_list': dvd_list}, RequestContext(request))


@login_required
@user_passes_test(lambda u: permissions.in_dvdadmin_group(u))
def dvd_add(request):
    previous = None
    if request.method == 'POST':
        name = request.POST['name']
        try:
            dvd = DVD.objects.get(name=name)
            previous = "Error: %s has already been added!" % name
        except DVD.DoesNotExist:
            sortname = request.POST['sortname']
            amountLeft = request.POST['amountLeft']
            imdbID = request.POST['imdbID']
            dvd = DVD(name=name, sortname=sortname, amountTotal=amountTotal, timesRented=0, amountLeft=amountTotal, imdbID=imdbID)
            dvd.save()
            previous = "%s was added successfully!" % name
    return render_to_response('dvd/dvd_add.html', {'previous': previous}, RequestContext(request))


@login_required
@user_passes_test(lambda u: permissions.in_dvdadmin_group(u))
def dvd_edit(request):
    DVD_list = DVD.objects.all().order_by('name')
    return render_to_response('dvd/dvd_edit.html', {'DVD_list': DVD_list}, RequestContext(request))

@login_required
@user_passes_test(lambda u: permissions.in_dvdadmin_group(u))
def dvd_edit_single(request, dvd_id):
    dvd = get_object_or_404(DVD, pk=dvd_id)
    change = False
    if (request.method == 'POST'):
        dvd = get_object_or_404(DVD, pk=dvd_id)
        dvd.name = request.POST['name']
        dvd.sortname = request.POST['sortname']
        dvd.amountTotal = request.POST['amountTotal']
        dvd.imdbID = request.POST['imdbID']
        dvd.save()
        change = True
    return render_to_response('dvd/dvd_edit_single.html', {'dvd': dvd, 'change': change}, RequestContext(request))

@login_required
@user_passes_test(lambda u: permissions.in_dvdadmin_group(u))
def dvd_delete(request, dvd_id):
    dvd = get_object_or_404(DVD, pk=dvd_id)
    dvdname = dvd.name
    rentalList = Rental.objects.filter(dvd = dvd)
    for rental in rentalList:
        rental.delete()
    dvd.delete()
    return render_to_response('dvd/dvd_delete.html', {'dvdname': dvdname}, RequestContext(request))


@login_required
@user_passes_test(lambda u: permissions.in_dvdadmin_group(u))
def addadmin(request):
    g = permissions.get_dvdadmin_group()
    if (request.method == 'POST'):
        netid = request.POST['netid']
        user_info = gdi(netid)
        if user_info is None:
            return render_to_response('dvd/user_not_found.html')

        try:
            user = User.objects.get(username=netid)
        except User.DoesNotExist:
            user = User(username=netid, password="") #Password doesn't matter with CAS!
        user.groups.add(g)
        user.save()
    dvdadmins  = [u.username for u in g.user_set.all()] + [u.username for u in User.objects.filter(is_superuser=True)]
    return render_to_response('dvd/addadmin.html', {'dvdadmins': dvdadmins}, context_instance=RequestContext(request))


def forbidden(request, template_name='403.html'):
    """Default 403 handler"""
    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request)))
