from .models import Timetable
from django import forms


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ["todo_id", "start", "end"]
