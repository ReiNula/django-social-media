from audioop import reverse
from re import template
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib import messages

from django.urls import reverse_lazy
from django.views.generic import View, CreateView, DetailView, ListView, FormView

from .forms import AddMessageForm, LikeForm, ReplyForm, RetweetForm, RegistrationForm
from .models import Hashtag, HashtagContent, Like, Message, Subscription, User


def LikeView(request, pk):
    # Amelioration : verify if someone already like a message

    message = get_object_or_404(Message, id=request.POST.get('message_id'))
    Like(message=message, user=request.user).save()
    return redirect('home')


class LoginPageView(auth_views.LoginView):
    template_name = "registration/login.html"

    def get(self, request):
        # Define view with GET method
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
    
    def post(self, request):
        # Define view with POST method
        form = self.get_form()
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                # Success login
                login(request, user)
                return redirect('home')
        message = 'Login failed, try again'
        return render(request, self.template_name, context={'form': form, 'message': message})


class LogoutPageView(auth_views.LogoutView):
    pass


class RegisterView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class IndexView(ListView):
    """
    Show last authenticated user + followed accounts messages
    and republished (not replies)
    """
    # queryset = Message.objects.order_by('-publication_date')
    model = Message
    context_object_name = 'messages'
    ordering = ['-publication_date']
    template_name = 'socialmedia/index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        followed_users = Subscription.objects.filter(follower=self.request.user).values('followed')
        context['followed_messages'] = Message.objects.filter(user__in=followed_users).order_by('-publication_date')
        return context


class DetailMessageView(DetailView):
    model = Message
    context_object_name = 'message'
    slug_field = 'origin_id'
    slug_url_kwarg = 'origin_id'
    template_name = 'socialmedia/message_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Message.objects.filter(origin=self.get_object()).order_by('-publication_date')
        context['likes'] = Like.objects.filter(message=self.get_object()).count()
        return context


class AddMessageView(CreateView):
    """
    Add new message from authenticated used
    """
    form_class = AddMessageForm
    success_url = reverse_lazy('home')
    template_name = 'socialmedia/new_message.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        form = self.get_form()
        if form.is_valid:
            form.save(user=request.user, commit=False)
        return redirect('home')


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
    success_url = reverse_lazy('home')
    template_name = 'socialmedia/retweet.html'


class ReplyView(CreateView):
    model = Message
    form_class = ReplyForm
    template_name = 'socialmedia/reply.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.origin = Message.objects.filter(id=self.kwargs['pk']).first()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_content'] = Message.objects.filter(id=self.kwargs['pk']).first()
        return context

    success_url = reverse_lazy('home')


class FollowView(View):
    model = Subscription

    def get(self, request, *args, **kwargs):
        pass


class HashtagView(DetailView):
    model = Hashtag
    context_object_name = 'hashtag'
    slug_field = 'name'
    slug_url_kwarg = 'name'
    template_name = 'socialmedia/hashtag.html'


class AlertView(ListView):
    pass