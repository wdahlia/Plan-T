from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager

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
    when = models.DateTimeField()
    started_at = models.CharField(max_length=5, null=True)
    expired_at = models.CharField(max_length=5, null=True)
    is_completed = models.BooleanField(default=False)
    tags = TaggableManager(
        verbose_name=("tags"),
        help_text=("쉼표로 태그를 구분합니다"),
        blank=True,
    )
