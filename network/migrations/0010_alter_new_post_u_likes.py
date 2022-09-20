# Generated by Django 4.0.6 on 2022-09-19 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_new_post_u_likes_alter_new_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new_post',
            name='u_likes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='u_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
