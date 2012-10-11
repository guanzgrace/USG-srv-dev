from django.contrib import admin

from models import Apps
admin.site.register(Apps)

from models import Categories
admin.site.register(Categories)

from models import Slideshow
admin.site.register(Slideshow)
