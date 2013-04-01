from django.db import models

class Appointment(models.Model):
    name = models.CharField(max_length=40)
    netid = models.CharField(max_length=15)
    time = models.DateTimeField()
    isActive = models.BooleanField(default=True)
    
    def __unicode__(self):
		return str(self.netid) + " " + str(self.time)
		