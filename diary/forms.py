from django import forms
from .models import Grade, Schedule

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'value']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['student', 'subject', 'day_of_week', 'time']
