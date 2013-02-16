from django.contrib.auth.models import Group

def get_dvdadmin_group():
    try:
        g = Group.objects.get(name='dvdadmin')
    except Group.DoesNotExist:
        g = Group(name='dvdadmin')
        #not sure how to add permissions, might as well just do it manually
        g.save()
    return g

def in_dvdadmin_group(u):
    if u is not None:
        return u.is_superuser or u.groups.filter(name='dvdadmin').exists()
    return False
