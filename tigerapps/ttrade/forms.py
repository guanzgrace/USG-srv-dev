from django import forms
from ttrade.models import *

class CreateForm(forms.ModelForm):
    class Meta:
        model=Listing
        fields = ('method', 'description', 'picture', 'price')

class ListingForm(forms.ModelForm):
    class Meta:
        model=Listing
        fields = ('category', 'method', 'title', 'description', 'picture', 'price')
