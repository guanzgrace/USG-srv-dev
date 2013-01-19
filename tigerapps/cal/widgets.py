from django import forms
from django.utils.safestring import mark_safe

class TagWidget(forms.TextInput):
	class Media:
		css = {
		}
		js = ('/static/cal/js/tags.js')
	
#	def __init__(self, attrs=None):
#		super(TagWidget, self).__init__(attrs)
		
#	def render(self, name, value, attrs=None):
#		return mark_safe(self.html)