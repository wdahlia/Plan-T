from django.db import models
from datetime import date, datetime
from django.conf import settings
from todos.models import Todos
from dateutil.relativedelta import relativedelta

# Create your models here.
now = datetime.now()


class Study(models.Model):
    category = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    desc = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    max_people = models.IntegerField()
    participated = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="participate"
    )
    start_at = models.DateField(auto_now_add=True)
    end_at = models.DateField(default=(now + relativedelta(months=6)))

    @property
    def is_activate(self):
        if self.end_at is None:
            return True
        else:
            return date.today() < self.end_date


class StudyTodo(Todos):
    study_pk = models.ForeignKey("Study", on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    when = None
    image = None
    tags = None
    started_at = None
    expired_at = None
