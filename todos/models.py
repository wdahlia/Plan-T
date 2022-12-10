from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Todos(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField()
    when = models.DateField()
    started_at = models.CharField(max_length=5, null=True)
    expired_at = models.CharField(max_length=5, null=True)
    is_completed = models.BooleanField(default=False)


class Tag(models.Model):
    todo = models.ForeignKey("Todos", on_delete=models.CASCADE, related_name="tagged")
    content = models.CharField(max_length=30)
