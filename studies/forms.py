from .models import StudyTodo
from django import forms


class StudyTodoForm(forms.ModelForm):
    class Meta:
        model = StudyTodo
        fields = [
            "title",
            "content",
        ]
