from django.db import models
from django.contrib import admin
from adminsortable.models import Sortable, SortableForeignKey

class Category(Sortable):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return unicode(self.name)

    class Meta(Sortable.Meta):
        verbose_name_plural = 'categories'

class App(Sortable):
    SLIDESHOW_INDICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    
    name = models.CharField(max_length=100)
    abbr_name = models.CharField(max_length=16, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
    icon = models.ImageField(upload_to='www/icons')
    category = SortableForeignKey(Category)

    featured_index = models.IntegerField(blank=True, null=True, choices=SLIDESHOW_INDICES, unique=True)
    n_views = models.IntegerField(default=0)

    description = models.TextField()
    screenshot = models.ImageField(upload_to='www/screenshot', blank=True, null=True)
    founder_description = models.TextField(blank=True, null=True)

    class Meta(Sortable.Meta):
        ordering = ['category__order', 'order']
    
    def __unicode__(self):
        return unicode(self.name)
