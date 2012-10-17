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
    
    title = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10, help_text='This will be used for the Slideshow Name', blank=True, null=True)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField()
    icon = models.ImageField(upload_to='icons', blank=True, null=True)
    slideshow_picture = models.ImageField(upload_to='slideshow', blank=True, null=True)
    number_of_views = models.IntegerField()
    category = SortableForeignKey(Category)
    slideshow_index = models.IntegerField(blank=True, null=True, choices=SLIDESHOW_INDICES, unique=True)
    url = models.CharField(max_length=1000)

    class Meta(Sortable.Meta):
        ordering = ['category__order', 'order']
    
    def __unicode__(self):
        return unicode(self.title)
