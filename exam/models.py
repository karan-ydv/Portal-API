import random
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from student.models import Profile

types = (
    ("1", "Aptitude"),
    ("2", "C"),
    ("3", "Java"),
    ("4", "BigData"),
    ("5", "Algo"),
)

options = (
    ("1", "A"),
    ("2", "B"),
    ("3", "C"),
    ("4", "D")
)

NUMBER_OF_PROBLEMS = 50

class Question(models.Model):
    statement = models.TextField(max_length=200, blank = False, default=None)
    code = models.TextField(blank=True)
    A = models.CharField(max_length = 100, blank = False)
    B = models.CharField(max_length = 100, blank = False)
    C = models.CharField(max_length = 100, blank = False)
    D = models.CharField(max_length = 100, blank = False)
    
    Type = models.CharField(max_length = 20, choices = types, default = '1')
    def __str__(self):
        return self.statement

class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    ans = models.CharField(
        max_length = 1,
        choices = options,
        blank=False,
        null=False
    )
    def __str__(self):
        return str(self.question.id)

def now_plus_30():
    return timezone.now() + timezone.timedelta(minutes=30)

def now_plus_10():
    return timezone.now() + timezone.timedelta(minutes=10)

def testCode():
    return random.randint(1000,9999)

class Test(models.Model):

    test_code = models.IntegerField(
        default = testCode,
        unique=True,
        primary_key=True
    )

    start_time = models.DateTimeField(default = now_plus_10)
    duration = models.PositiveIntegerField(default = 30)
    examinees = models.ManyToManyField(
        Profile,
        related_name='tests',
        blank = True
    )

    questions = models.ManyToManyField( Question, related_name='questions')
    corr_score = models.PositiveIntegerField(
        verbose_name="Score for correct ans",
        default=4,
        blank=False
    )

    wrong_score = models.IntegerField(
        verbose_name="Score for wrong ans",
        default=0,
        validators= [MaxValueValidator(0)],
        blank=False
    )

    def __str__(self):
        return str(self.test_code)

class Response(models.Model):
    student = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='response'
    )

    test_code = models.IntegerField()
    score = models.IntegerField(default=0)
    def __str__(self):
        return self.student.user.username

question_labels = [ ('Q' + str(i)) for i in range(1,NUMBER_OF_PROBLEMS+1) ]
for label in question_labels:
    Response.add_to_class(label, models.CharField(max_length=1, choices=options, blank=True, null=True))