from django.db import models
from django.contrib import admin

class Category (models.Model):
    name = models.CharField(max_length=100)
    index = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name_plural = 'categories'

class App (models.Model):
    name = models.CharField(max_length=100)
    abbr_name = models.CharField(max_length=10, blank=True, null=True)
    url = models.CharField(max_length=1000)
    icon = models.ImageField(upload_to='icons', blank=True, null=True)
    description = models.TextField()
    
    category = models.ForeignKey(Category)
    category_index = models.IntegerField()
    slideshow_picture = models.ImageField(upload_to='slideshow', blank=True, null=True)
    slideshow_index = models.IntegerField(blank=True, null=True)
    n_views = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'%s %s %s' %(self.title, self.id, self.category.name)
