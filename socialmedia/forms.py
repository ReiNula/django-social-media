from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Like, Message, User

class RegistrationForm(UserCreationForm):
    # Create user registration

    class Meta:
        model = User
        fields = ('username', 'email')


class AddMessageForm(forms.ModelForm):
    
    class Meta:
        model = Message
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(AddMessageForm, self).save(**kwargs)
        instance.user = user
        instance.save()
        return instance



class RetweetForm(forms.ModelForm):
    
    class Meta:
        model = Message
        fields = ('user', 'retweeted', 'content')


class ReplyForm(forms.ModelForm):
    
    class Meta:
        model = Message
        # fields = ('user', 'origin', 'content')
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class LikeForm(forms.ModelForm):

    class Meta:
        model = Like
        fields = ('user', 'message')