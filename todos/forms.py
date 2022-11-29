from django import forms
from .models import Todos, Timetable


class TodosForm(forms.ModelForm):
    class Meta:
        model = Todos
        fields = [
            "title",
            "content",
            "image",
        ]
