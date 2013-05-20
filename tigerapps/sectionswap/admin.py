from django.contrib import admin
from pounce.models import Course, Class, Subscription

class CourseAdmin(admin.ModelAdmin):
	fields = ('code', 'title', 'number')
	search_fields = ('code', 'title')
	
class ClassAdmin(admin.ModelAdmin):
	fields = ('course', 'title', 'number', 'time', 'days', 'enroll', 'max', 'isClosed')
	search_fields = ('course__code', 'course__title', 'title')
	
class SubscriptionAdmin(admin.ModelAdmin):
	fields = ('theclass', 'address', 'type', 'active')
	search_fields = ('theclass__course__code',)
	
admin.site.register(Course, CourseAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Subscription, SubscriptionAdmin)