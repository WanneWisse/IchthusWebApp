from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location_url = models.CharField(max_length=200)
    location_name = models.CharField(max_length=200)
    users = models.ManyToManyField(User, through='UserEvent')

class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Question(models.Model):
    text = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class UserQuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    userevent = models.ForeignKey(UserEvent, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)

class Tickie(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=1000)
    image_type = models.CharField(max_length=100)
    image = models.CharField(max_length=10000000)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class UserTickieAnswer(models.Model):
    tickie = models.ForeignKey(Tickie, on_delete=models.CASCADE)
    userevent = models.ForeignKey(UserEvent, on_delete=models.CASCADE)