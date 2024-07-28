from django.db import models
from django.utils import timezone

class User(models.Model):
 name = models.CharField(max_length=20)
 login = models.CharField(max_length=20) # login name
 password = models.CharField(max_length=255, default='defaultpassword') 
 icon = models.ImageField(default='blog/icon/default_icon.png',upload_to = 'blog/icon/')
 profile = models.TextField(default='Nice to meet you!')
 
class Blog(models.Model):
 author = models.ForeignKey(User,
 on_delete=models.CASCADE)
 timeslot = models.DateTimeField(default=timezone.now)  # default value = current time
 content = models.TextField()
 title = models.CharField(max_length=30)
 photos = models.ImageField(null=True, blank=True)