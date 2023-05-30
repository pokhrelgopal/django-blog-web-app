from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to='profile/')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

class Post(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='post/')
    caption = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.title)
