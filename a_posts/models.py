from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import FileExtensionValidator 
from django.core.exceptions import ValidationError
# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=500)
    image= models.ImageField(upload_to='social_post_images',null=True,blank=True)
    video=models.FileField(upload_to='social_post_video', null=True,default='',blank=True,
            validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='posts')
    body=models.TextField()
    likes=models.ManyToManyField(User,related_name='likedposts',through='LikedPost')
    tags=models.ManyToManyField('Tag',blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100,default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        return str(self.author)
    
class LikedPost(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    def __srt__(self):
        return f'{self.user.username}:{self.post.title}'

class Tag(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)
    def __str__(self):
        return self.name
    


class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='comments')
    parent_post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    body=models.CharField(max_length=150)
    likes=models.ManyToManyField(User,related_name='likedcomments',through='LikedComment')
    created=models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100,default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        try:
            return f'{self.author.username}:{self.body[:30]}'
        except:
            return f'no author:{self.body[:30]}'
    class Meta:
        ordering=['-created']

    
class LikedComment(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    def __srt__(self):
        return f'{self.user.username}:{self.comment.body}'

class Reply(models.Model):
    author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='replies')
    parent_comment=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='replies')
    body=models.CharField(max_length=150)
    likes=models.ManyToManyField(User,related_name='likedreplies',through='LikedReply')
    created=models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100,default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        try:
            return f'{self.author.username}:{self.body[:30]}'
        except:
            return f'no author:{self.body[:30]}'
    class Meta:
        ordering=['-created']


    
class LikedReply(models.Model):
    reply=models.ForeignKey(Reply,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    def __srt__(self):
        return f'{self.user.username}:{self.reply.body}'
