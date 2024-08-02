from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile/',null=True,blank=True,default='a_posts/images/avatar_default.svg')
    realname=models.CharField(max_length=59,null=True,blank=True)
    email=models.EmailField(unique=True,null=True)
    location=models.CharField(max_length=20,null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)
    

    @property
    def avatar(self):
        try:
            avatar=self.image.url
        except:
            avatar=static('a_posts/images/avatar_default.suv')
        return avatar

    @property
    def name(self):
        try:
            name=self.realname
        except:
            name=self.user.username
        return name