from tkinter import CASCADE
from turtle import ondrag
from unicodedata import name
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser


# User model
class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True)
    biography = models.CharField(max_length=160, blank=True)


class Message(models.Model):
    content = models.CharField(max_length=280, blank=True)
    publication_date = models.DateField(auto_now_add=True)
    retweeted = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='retweets')
    origin = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        if self.content:
            return f'{self.content}, publié le {self.publication_date}'
        else:
            return f'Retweet {self.origin}'
    
    @property
    def total_likes(self):
        return Like.objects.filter(message=self).count()

    def clean(self):
        if not self.retweeted and not self.content:
            raise ValidationError('Have to write something to publish content')


class Like(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Subscription(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followeds')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def clean(self):
        if self.follower == self.followed:
            raise ValidationError('You cannot follow youself :(')


class Mention(models.Model):
    is_seen = models.BooleanField(default=False)
    mentionner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentionneds')
    mentionned = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentionners')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)


class Hashtag(models.Model):
    name = models.CharField(max_length=100)


class HashtagContent(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)