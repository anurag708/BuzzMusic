from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Album(models.Model):
    album_name=models.CharField(max_length=200)
    album_logo=models.CharField(max_length=2000)
    album_artist=models.CharField(max_length=200)
    album_genre=models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.album_name


class Song(models.Model):
    name=models.CharField(max_length=200)
    album=models.ForeignKey(Album,on_delete=models.CASCADE)
    song_link=models.CharField(max_length=5000,blank=None)
    def __str__(self):
        return self.name


class Like(models.Model):
    song=models.ForeignKey(Song,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    like=models.BooleanField(default=False)
    def __str__(self):
        if self.like:
            return self.user.username+" likes "+self.song.name
        else:
            return self.user.username+" dislikes "+self.song.name


class Comment(models.Model):
    comment=models.TextField()
    song=models.ForeignKey(Song,on_delete=models.CASCADE)
    def __str__(self):
        return self.comment


class Feedback(models.Model):
    feed=models.TextField()
    def __str__(self):
        return self.feed



        

