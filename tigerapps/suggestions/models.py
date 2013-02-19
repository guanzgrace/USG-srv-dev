from django.db import models
from datetime import datetime

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Voter(models.Model):
    user_netid      = models.CharField(max_length=12)
    user_firstname  = models.CharField('First Name', max_length=45)
    user_lastname   = models.CharField('Last Name', max_length=45)
    is_anonymous    = models.BooleanField(default = False)
    available_votes = models.IntegerField(default=5)
    user_last_login = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.user_netid

    def logged_in(self):
        self.user_last_login = datetime.now()
        self.save()

# A suggestion to be voted on.
class Suggestion(models.Model):
    title        = models.CharField(max_length=200)
    description  = models.TextField()
    creator      = models.ForeignKey(Voter)
    date_created = models.DateTimeField(default=datetime.now())
    vote_count   = models.IntegerField(default = 0)
    is_chosen    = models.BooleanField(default = False)
    is_completed = models.BooleanField(default = False)
    tags         = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.title

    def increment(self):
        self.vote_count += 1
        self.save()

class Vote(models.Model):
    cast_for  = models.ForeignKey(Suggestion)
    cast_by   = models.ForeignKey(Voter)
    date_cast = models.DateTimeField(default = datetime.now())

    def __unicode__(self):
        return cast_for
