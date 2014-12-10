from django.db import models
import ast

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    netID = models.CharField(max_length=8, unique=True)
    agenda_visibility = models.BooleanField(default=False)

    def blocks(self):
        blks = []
        for course in self.course_set.all():
            for blk in course.blocks:
                blks.append(blk)
        return blks
    
    def isScheduleConsistent(self):
        blks = self.blocks()
        return len(blks) == len(set(blks))

    def whyScheduleInconsistent(self):
    # Returns a tuple of conflicting courses, if any
    # Does not identify more than one conflict at a time
        if self.isScheduleConsistent():
            return
        for course1 in self.course_set.all():
            for course2 in self.course_set.all():
                if course1 == course2:
                    break
                for block2 in course2.blocks:
                    if block2 in course1.blocks:
                        return (course1, course2)
        raise RuntimeException('Should have found conflicting courses.')

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.netID

class Instructor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    netID = models.CharField(max_length=8, unique=True)
    faculty = models.BooleanField(default=False)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.netID
    
    def billable(self):
        if self.faculty:
            return 0
        my_courses = self.course_set.all()
        hours = 0.0
        for course in my_courses:
            hours += len(course.blocks)/2.0
        return hours
    
    def full_name(self):
        return self.first_name+" "+self.last_name

class Course(models.Model):
    courseID = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=150,default='Title needed')
    description = models.TextField(max_length=1000)
    other_section = models.ManyToManyField('self', blank=True, symmetrical=True)
    min_enroll = models.IntegerField(default=0)
    max_enroll = models.IntegerField(default=200)
    cancelled = models.BooleanField(default=False)
    room = models.CharField(max_length=200,default='tbd')
    blocks = ListField('Course blocks')
    schedule = models.CharField(max_length=50)
    students = models.ManyToManyField(Student, through='Registration')
    instructors = models.ManyToManyField(Instructor)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.courseID

    def current_enroll(self):
        return len(self.students.all())

    def is_full(self):
        num_enroll = self.current_enroll()
        return num_enroll >= self.max_enroll

    def meets_min_requirements(self):
        num_enroll = self.current_enroll()
        return num_enroll >= self.min_enroll
    
    def get_instructors(self):
        return ", ".join([i.full_name() for i in self.instructors.all()])
    
    is_full.boolean = True
    meets_min_requirements.boolean = True

class Registration(models.Model):
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course)
    timestamp = models.DateTimeField('Registration timestamp',auto_now_add=True)
    
    attendance_M = models.BooleanField(default=False)
    attendance_Tu = models.BooleanField(default=False)
    attendance_W = models.BooleanField(default=False)
    attendance_Th = models.BooleanField(default=False)
    attendance_F = models.BooleanField(default=False)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.student.netID+"-"+self.course.courseID
