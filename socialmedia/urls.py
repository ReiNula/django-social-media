from django.contrib import admin
from django.urls import path
from .views import AddMessageView, DetailTweetView, HashtagView, IndexView, LikeView, ReplyView, RetweetView, SignUpView, UserProfileView

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', IndexView.as_view(), name='index'),
    path('new/', AddMessageView.as_view(), name='new_message'),
    path('retweet/', RetweetView.as_view(), name='retweet'),
    path('reply/', ReplyView.as_view(), name='reply'),
    path('like/<int:pk>/', LikeView.as_view(), name='like'),
    path('hashtag/<str:name>', HashtagView.as_view(), name='hashtag'),
    path('<int:pk>/', DetailTweetView.as_view(), name='message_detail'),
    path('<str:username>/', UserProfileView.as_view(), name='profile'),
    
]