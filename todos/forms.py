from .models import Todos, Timetable
from django import forms


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ["todo_id", "start", "end"]

class TodosForm(forms.ModelForm):
    class Meta:
        model = Todos
        fields = [
            "title",
            "content",
            "image",
        ]
