from .models import Todos, Timetable
from django import forms


class TodosForm(forms.ModelForm):
    class Meta:
        model = Todos
        fields = [
            "title",
            "content",
            "image",
            # "started_at",
            # "expired_at",
        ]


# "started_at"


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ["todo_id", "start", "end"]
