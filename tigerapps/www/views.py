from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django_cas.decorators import user_passes_test
from django.contrib.auth.models import User
from www.models import *

def index(request):
    grouped_apps = []
    categories = Category.objects.all()
    for category in categories:
        apps = App.objects.filter(category=category)
        grouped_apps.append((category, apps))
    return render_to_response('www/index.html', {'grouped_apps': grouped_apps})

