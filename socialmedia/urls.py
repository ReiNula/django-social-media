from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import AddMessageView, DetailMessageView, HashtagView, IndexView, LikeView, ReplyView, RetweetView, RegisterView, UserProfileView, LoginPageView
urlpatterns = [
    path('admin/', admin.site.urls),  
    # path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', IndexView.as_view(), name='home'),
    path('new/', AddMessageView.as_view(), name='new_message'),
    path('retweet/', RetweetView.as_view(), name='retweet'),
    path('reply/<int:pk>/', ReplyView.as_view(), name='reply'),
    path('like/<int:pk>/', LikeView, name='like'),
    path('hashtag/<str:name>', HashtagView.as_view(), name='hashtag'),
    path('<int:pk>/', DetailMessageView.as_view(), name='message_detail'),
    path('profile-<str:username>/', UserProfileView.as_view(), name='profile'),
]