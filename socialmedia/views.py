from re import template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import AddMessageForm, LikeForm, ReplyForm, RetweetForm, UserSignIn
from .models import Hashtag, HashtagContent, Like, Message, Subscription, User


# Sign In View
class SignUpView(CreateView):
    form_class = UserSignIn
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class IndexView(ListView):
    """
    Affiche les derniers messages de l'utilisateur + abonnés
    et retweets (n'affiche pas les réponses)
    """
    queryset = Message.objects.order_by('-publication_date')
    context_object_name = 'messages'
    template_name = 'socialmedia/index.html'


class AddMessageView(CreateView):
    """
    Ajoute un nouveau message de l'utilisateur à la date du jour
    """
    form_class = AddMessageForm
    success_url = reverse_lazy('index')
    # fields = ['user','content']
    template_name = 'socialmedia/new_message.html'


class UserProfileView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'socialmedia/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_messages'] = Message.objects.filter(user=self.get_object()).order_by('-publication_date')
        context['followers'] = Subscription.objects.filter(followed=self.get_object()).count()
        context['followeds'] = Subscription.objects.filter(follower=self.get_object()).count()
        context['nb_published_messages'] = Message.objects.filter(user=self.get_object()).count()
        return context


class RetweetView(CreateView):
    form_class = RetweetForm
    success_url = reverse_lazy('index')
    template_name = 'socialmedia/retweet.html'


class ReplyView(CreateView):
    form_class = ReplyForm
    success_url = reverse_lazy('index')
    template_name = 'socialmedia/reply.html'


class DetailTweetView(DetailView):
    model = Message
    context_object_name = 'message'
    slug_field = 'origin_id'
    slug_url_kwarg = 'origin_id'
    template_name = 'socialmedia/message_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Message.objects.filter(origin=self.get_object()).order_by('-publication_date')
        return context


class LikeView(CreateView):
    # TODO Améliorer en likant sur le message par la clé étrangère
    form_class = LikeForm
    success_url = reverse_lazy('index')
    context_object_name = 'message'
    slug_field = 'message_id'
    slug_url_kwarg = 'message_id'
    template_name = 'socialmedia/like.html'

    def get_queryset(self):
        print(get_object_or_404(Message, id=self.kwargs[0]))

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['liked_message'] = self.message
    #     return context


class HashtagView(DetailView):
    model = Hashtag
    context_object_name = 'hashtag'
    slug_field = 'name'
    slug_url_kwarg = 'name'
    template_name = 'socialmedia/hashtag.html'


class AlertView(ListView):
    pass