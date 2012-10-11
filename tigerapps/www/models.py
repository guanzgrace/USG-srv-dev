from django.db import models
class Categories (models.Model):
    name = models.TextField(max_length = 100)
    list_index = models.CommaSeparatedIntegerField(max_length=100)
    category_index = models.IntegerField()
    def __unicode__(self):
            return u'%s %s' %(self.name, self.id)

class Apps (models.Model):
    title = models.TextField(max_length = 100)
    abbreviation = models.CharField(max_length = 10, help_text="This will be used for the Slideshow Name")
    short_description = models.TextField(max_length= 500)
    long_description = models.TextField(max_length= 65000)
    icon = models.ImageField(upload_to = 'icons')
    slideshow_picture = models.ImageField(upload_to = 'slideshow')
    number_of_views = models.IntegerField()
    category = models.ForeignKey(Categories)
    slideshow_index = models.IntegerField(max_length=100, blank = True)
    url = models.TextField(max_length= 1000)
    def __unicode__(self):
            return u'%s %s %s' %(self.title, self.id, self.category.name)

class Slideshow (models.Model):
    first_slide = models.ForeignKey(Apps, blank = True, related_name ='one')
    second_slide = models.ForeignKey(Apps, blank = True, related_name ='two')
    third_slide = models.ForeignKey(Apps, blank = True, related_name ='three')
    fourth_slide = models.ForeignKey(Apps, blank = True, related_name ='four')
    fifth_slide = models.ForeignKey(Apps, blank = True, related_name ='five' )
    sixth_slide = models.ForeignKey(Apps, blank = True, related_name ='six')
    seventh_slide = models.ForeignKey(Apps, blank = True, related_name ='seven')
    eighth_slide = models.ForeignKey(Apps, blank = True, related_name ='eight')
    ninth_slide = models.ForeignKey(Apps, blank = True, related_name ='nine')
    tenth_slide = models.ForeignKey(Apps, blank = True, related_name ='ten')
    def __unicode__(self):
            return u'%s %s %s %s' %(self.id, first_slide.id, second_slide.id, third_slide.id)
