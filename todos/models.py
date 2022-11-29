from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Todos(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField()
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 80},
    )
    started_at = models.DateTimeField(blank=True)
    expired_at = models.DateTimeField(blank=True)


class Timetable(models.Model):
    todo_id = models.ForeignKey("Todos", on_delete=models.CASCADE)
    today = models.DateTimeField(auto_now_add=True)
    start = models.IntegerField()
    end = models.IntegerField()
