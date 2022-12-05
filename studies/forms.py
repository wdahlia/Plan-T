
from django import forms
from .models import Study
from .models import StudyTodo

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = [
            "category",
            "title",
            "max_people",
            "desc",
        ]

class StudyTodoForm(forms.ModelForm):
    class Meta:
        model = StudyTodo
        fields = [
            "title",
            "content",
        ]
