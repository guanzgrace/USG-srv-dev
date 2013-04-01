from django.db import models

class Appointment(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    time = models.DateTimeField()
    isActive = models.BooleanField(default=True)
    
    def __unicode__(self):
		return str(self.name) + " " + str(self.time)
		