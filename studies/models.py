from django.db import models
from datetime import datetime
from django.conf import settings

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
    do = models.ManyToManyField("Study_Todo")
    start_at = models.DateField()
    end_at = models.DateField()

    @property
    def is_activate(self):
        return datetime.now() > self.end_date


class Study_Todo(models.Model):
    study_pk = models.ForeignKey("Study", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    complete = models.BooleanField(default=False)
