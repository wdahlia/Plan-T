
from django import forms
from .models import Study


class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = [
            "category",
            "title",
            "max_people",
            "desc",

class StudyTodoForm(forms.ModelForm):
    class Meta:
        model = StudyTodo
        fields = [
            "title",
            "content",
        ]
