from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import suggestions.models as models

@login_required(login_url="/suggestions/login/")
def main_page(request):
    netid = request.META['USER']
    if (models.Voter.objects.filter(user_netid = netid).exists()):
        models.Voter.objects.get(user_netid = netid).logged_in()
        print "in there"
    else:
        v = models.Voter(user_netid = netid)
        v.save()
        print "not in there"

    return render_to_response("www/suggestions.html",
                              {
                                "netid" : netid, 
                              },
                              RequestContext(request)
                             )
