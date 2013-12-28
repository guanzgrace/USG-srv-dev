from django.contrib import admin
from wintersession.models import Student,Instructor,Course,Registration
from django import forms

class RegistrationInline(admin.TabularInline):
    model = Registration

class StudentAdmin(admin.ModelAdmin):
    inlines = [RegistrationInline]
    list_display = ('netID','first_name','last_name')
#    list_filter = ['last_name']
    search_fields = ['netID']

admin.site.register(Student, StudentAdmin)

class CourseInstructorInline(admin.TabularInline):
    model = Course.instructors.through #@UndefinedVariable

class InstructorAdmin(admin.ModelAdmin):
    inlines = [CourseInstructorInline]
    list_display = ('netID','first_name','last_name','billable')
#    list_filter = ['last_name']
    search_fields = ['netID']

admin.site.register(Instructor, InstructorAdmin)

class OtherSectionInline(admin.TabularInline):
    model = Course.other_section.through #@UndefinedVariable
    fk_name = 'from_course'
    extra = 1
    verbose_name = "Other section of the same course"
    verbose_name_plural = "Other sections of the same course"
    
# Makes the blocks (a ListField which is subclass of TextField defaults Textarea)
# into a TextInput
class BlocksModelForm( forms.ModelForm ):
    blocks = forms.CharField( widget=forms.TextInput )
    class Meta:
        model = Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseID','title','schedule','current_enroll',
                    'max_enroll', 'meets_min_requirements','cancelled')
    exclude = ('instructors', 'other_section',)
#    list_filter = ['meets_min_requirements','cancelled']
    search_fields = ['courseID','title']
    inlines = [OtherSectionInline, CourseInstructorInline]
    form = BlocksModelForm

admin.site.register(Course, CourseAdmin)

class RegistrationAdmin(admin.ModelAdmin):
#   fields = ['student', 'course', 'timestamp']
    list_display = ('course','student')
#    list_filter = ['course','student']
    search_fields = ['course__courseID','student__netID']
 
admin.site.register(Registration, RegistrationAdmin)

