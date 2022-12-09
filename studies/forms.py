from django import forms
from .models import Study
from .models import StudyTodos


class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = [
            "category",
            "title",
            "max_people",
            "desc",
        ]


class StudyTodosForm(forms.ModelForm):
    class Meta:
        model = StudyTodos
        fields = [
            "title",
            "content",
            "start",
            "end",
        ]
