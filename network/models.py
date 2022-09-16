import re
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    followers_number = models.IntegerField(default=0)
    following_number = models.IntegerField(default=0)
    followers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="u_followers")
    following = models.ManyToManyField("self", blank=True,  symmetrical=False, related_name="u_following")


class New_post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    post = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.post}"
    
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.id,
            "post": self.post,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }

