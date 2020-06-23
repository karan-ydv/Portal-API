from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

branches = (
    ("1", "CSE"),
    ("2", "IT"),
    ("3", "EC")
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_number = models.IntegerField(
        # name = "Student Number",
        primary_key = True,
        unique = True,
        validators = [
            MaxValueValidator(1980000),
            MinValueValidator(1910000)
        ]
    )
    branch = models.CharField(max_length=50, choices = branches)

    def __str__(self):
        return str(self.user.username)
        # return self.user.name
