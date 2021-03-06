# Generated by Django 4.0.1 on 2022-02-15 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0003_rename_name_hashtagcontent_hashtag'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='retweeted',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='retweets', to='socialmedia.message'),
        ),
        migrations.AlterField(
            model_name='mention',
            name='mentionned',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentionners', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mention',
            name='mentionner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentionneds', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='socialmedia.message'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='followed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followeds', to=settings.AUTH_USER_MODEL),
        ),
    ]
