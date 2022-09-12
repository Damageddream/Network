# Generated by Django 4.0.6 on 2022-09-11 09:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_user_followers_number_user_following_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='u_followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='u_following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Following',
        ),
    ]