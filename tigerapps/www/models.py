from django.db import models
from django.contrib import admin

class Category (models.Model):
    name = models.CharField(max_length=100)
    index = models.IntegerField()
    
    def __unicode__(self):
        return u'%s %s' %(self.name, self.id)

    class Meta:
        verbose_name_plural = 'categories'

class App (models.Model):
    title = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10, help_text='This will be used for the Slideshow Name', blank=True, null=True)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField()
    icon = models.ImageField(upload_to='icons', blank=True, null=True)
    slideshow_picture = models.ImageField(upload_to='slideshow', blank=True, null=True)
    number_of_views = models.IntegerField()
    category = models.ForeignKey(Category)
    slideshow_index = models.IntegerField(blank=True, null=True)
    category_index = models.IntegerField()
    url = models.CharField(max_length=1000)
    
    def __unicode__(self):
        return u'%s %s %s' %(self.title, self.id, self.category.name)
