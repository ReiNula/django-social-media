from dataclasses import fields
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserSignIn
from .models import User, Message, Like, Subscription, Mention, Hashtag, HashtagContent

# Admin model
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional fields", {'fields': ('birthday', 'biography')}),
    )


class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'content', 'origin', 'retweeted')}),
    )
    list_display = ('user', 'content', 'origin', 'retweeted')


class LikeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('message', 'user')}),
    )
    list_display = ('user', 'message',)


class SubscriptionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('follower', 'followed')}),
    )
    list_display = ('follower', 'followed',)


class HashtagAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
    )
    list_display = ('name',)


class HashtagContentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('message', 'hashtag')}),
    )
    list_display = ('hashtag', 'message',)


class MentionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Content information', {'fields': ('mentionner', 'mentionned', 'message')}),
        ('Check seen by mentionned', {'fields': ('is_seen',)}),
    )
    list_display = ('mentionner', 'mentionned', 'message', 'is_seen')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Mention, MentionAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(HashtagContent, HashtagContentAdmin)