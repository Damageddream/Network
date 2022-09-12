# Generated by Django 4.0.6 on 2022-09-10 14:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_new_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='following_number',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
