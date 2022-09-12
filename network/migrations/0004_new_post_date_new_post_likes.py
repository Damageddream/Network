# Generated by Django 4.0.6 on 2022-09-10 12:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_rename_post_new_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_post',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='new_post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]