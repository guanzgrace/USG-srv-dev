from django.contrib import admin

from models import App
admin.site.register(App)

from models import Category
admin.site.register(Category)

from models import Slideshow
admin.site.register(Slideshow)
