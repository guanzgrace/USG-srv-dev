from django.db import models

class Course(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=128)
    number = models.CharField(max_length=30, primary_key=True)
    hits = models.IntegerField(default=0) # times requested; for diagnostics
    # section_set (ForeignKey)
    
    def __eq__(self, other):
        if other:
	    return self.number == other.number
        return None
        	
    def __ne__(self, other):
        if other:
            return not self.__eq__(other)
        return None
    
    def __unicode__(self):
        return self.short_name() + ' | ' + self.name
    
    def short_name(self):
        return self.code
    
class Section(models.Model):
    number = models.CharField(max_length=30, primary_key=True)
    course = models.ForeignKey(Course)
    name   = models.CharField(max_length=4)
    days   = models.CharField(max_length=15)
    time   = models.CharField(max_length=19)
    max = models.IntegerField(default=1000)
    enroll = models.IntegerField(default=0)
    isClosed = models.BooleanField(default=False)
    
    # TODO: use something less expensive than str compare
    def __eq__(self, other):
        return type(self) == type(other) \
            and unicode(self) == unicode(other)
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __unicode__(self):
        return self.course.short_name() + ' ' + self.name
    
    def sorted_had_by_set(self):
        return sorted(self.had_by_set.all())

class Entry(models.Model):
    courseNumber = models.CharField(max_length=30)
    section = models.CharField(max_length=30)
    totalEnroll = models.IntegerField(default=0)
    totalClosed = models.BooleanField(default=False)	
    
class User(models.Model):
    netid = models.CharField(max_length=8)
    pwd   = models.CharField(max_length=32)
    # swaprequest_set (ForeignKey)
    
    def __eq__(self, other):
        return self.netid == other.netid
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __unicode__(self):
        return self.netid

class SwapRequest(models.Model):
    user = models.ForeignKey(User)
    have = models.ForeignKey(Section, related_name='had_by_set')
    want = models.ForeignKey(Section, related_name='wanted_by_set')
    date = models.DateTimeField(auto_now=True)
    
    def __gt__(self, other):
        return self.date > other.date

    def __ge__(self, other):
        return self.date >= other.date

    def __lt__(self, other):
        return self.date < other.date

    def __le__(self, other):
        return self.date <= other.date

    def __eq__(self, other):
        return type(self) == type(other) \
            and self.user == other.user \
            and self.have == other.have \
            and self.want == other.want

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        result = 17
        result = 31 * result + hash(self.user.netid)
        result = 31 * result + hash(self.have.name)
        result = 31 * result + hash(self.want.name)
        return result

    def __unicode__(self):
        return unicode(self.user) + ": " + str(self.have) + " -> " + str(self.want) 
    
    def find_cycle(self, visited_list=None, visited_set=None):
        if visited_list == None:
            visited_list = []
        if visited_set == None:
            visited_set = set()
        
        visited_list.append(self)
        visited_set.add(self)
        
        for req in self.want.sorted_had_by_set():
            if req == visited_list[0]:
                return visited_list
	    if req not in visited_set:
                temp = req.find_cycle(visited_list[:], set(visited_set))
            if temp != None:
                return temp
