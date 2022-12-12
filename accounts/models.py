from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from studies.models import Study
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        ('username'),
        max_length=14,
        unique=True,
        help_text= ('Required. 14 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    nickname = models.CharField(max_length=14, null=True, blank=True)
    image = ProcessedImageField(
        upload_to="images/",
        null=True,
        blank=True,
        processors=[ResizeToFill(150, 150)],
        format="JPEG",
        options={"quality": 80},
    )
    join_study = models.ManyToManyField(Study, related_name="joined_study")
