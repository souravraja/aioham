# Generated by Django 5.0.6 on 2024-07-23 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("a_posts", "0002_post_artist_post_url"),
    ]

    operations = [
        migrations.RemoveField(model_name="post", name="artist",),
        migrations.RemoveField(model_name="post", name="url",),
    ]
