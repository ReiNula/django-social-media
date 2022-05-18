from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Like, Message, User

class UserSignIn(UserCreationForm):
    # Create user sign in

    class Meta:
        model = User
        fields = ('username', 'email')


class AddMessageForm(forms.ModelForm):
    
    class Meta:
        model = Message
        fields = ('user', 'content')


class RetweetForm(forms.ModelForm):
    
    class Meta:
        model = Message
        fields = ('user', 'retweeted', 'content')


class ReplyForm(forms.ModelForm):
    
    class Meta:
        model = Message
        fields = ('user', 'origin', 'content')


class LikeForm(forms.ModelForm):

    class Meta:
        model = Like
        fields = ('user', 'message')
