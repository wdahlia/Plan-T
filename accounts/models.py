from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from studies.models import Study

# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None

    nickname = models.CharField(max_length=500, null=True, blank=True)
    image = ProcessedImageField(
        upload_to="images/",
        null=True,
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 80},
    )
    join_study = models.ManyToManyField(Study, related_name="joined_study")
