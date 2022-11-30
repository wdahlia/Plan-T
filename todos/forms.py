from .models import Todos
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

