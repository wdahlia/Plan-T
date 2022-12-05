from django.db import models
from datetime import date
from django.conf import settings
from todos.models import Todos

# Create your models here.


class Study(models.Model):
    category_choice = (
        (1, "발표"),
        (2, "생활"),
        (3, "어학"),
    )
    category = models.IntegerField(choices=category_choice)
    title = models.CharField(max_length=50)
    desc = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    max_people = models.IntegerField()
    participated = models.ManyToManyField(
        settings.AUTH_USER_MODEL, symmetrical=True, related_name="participate"
    )
    start_at = models.DateField(default=date.today)
    end_at = models.DateField(null=True, blank=True)

    @property
    def is_activate(self):
        if self.end_at is None:
            return True
        else:
            return datetime.now() < self.end_date


class Study_Todo(Todos):
    study_pk = models.ForeignKey("Study", on_delete=models.CASCADE)
    image = None
