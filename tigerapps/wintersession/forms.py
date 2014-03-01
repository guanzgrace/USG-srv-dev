from django.forms import ModelForm, Form, CharField
from wintersession.models import Registration, Student

class AttendanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.fields['attendance_M'].label = 'M'
        self.fields['attendance_Tu'].label = 'Tu'
        self.fields['attendance_W'].label = 'W'
        self.fields['attendance_Th'].label = 'Th'
        self.fields['attendance_F'].label = 'F'
#         self.fields['student'].label = 'netID'
    class Meta:
        model = Registration
        fields = ['attendance_M', 'attendance_Tu', 'attendance_W',
                     'attendance_Th', 'attendance_F',]
#         widgets = {
#             'student': Select(attrs={'disabled':'true', 'readonly':'readonly'}),
#         }
        
class AgendaPrivacyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgendaPrivacyForm, self).__init__(*args, **kwargs)
        self.fields['agenda_visibility'].label = 'Make my agenda visible to all logged-in users'
         
    class Meta:
        model = Student
        fields = ['agenda_visibility',]

class FriendAgendaForm(Form):
    friend_netID = CharField(max_length=8)
