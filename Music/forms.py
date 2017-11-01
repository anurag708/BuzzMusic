from django import forms
from .models import Album,Song,Comment,Feedback
from django.contrib.auth.models import User

class AddSong(forms.ModelForm):
    class Meta:
        model=Song
        fields=['name','album','song_link']

class AddAlbum(forms.ModelForm):
    class Meta:
        model=Album
        fields=['album_name','album_logo','album_artist','album_genre']

class AddComment(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['comment']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields=['feed']
