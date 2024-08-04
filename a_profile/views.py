from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import *
from django.db.models import Count
from a_posts.forms import*
from django.contrib.auth.models import User,auth
# Create your views here.

def profile_view(request,username=None):
    if username:
        profile=get_object_or_404(User,username=username).profile
    else:
        try:
            profile=request.user.profile
        except:
            raise Http404()
    posts = profile.user.posts.all()
    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            # return render(request, 'a_profile/loop_profile_post.html', { 'posts': posts})
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            replyform = ReplyCreateForm()
            return render(request, 'a_profile/loop_profile_comments.html', { 'comments': comments, 'replyform': replyform })
        elif 'liked-posts' in request.GET:
            posts = profile.user.likedposts.order_by('-likedpost__created')  
        return render(request,'a_profile/loop_profile_post.html', {'posts': posts})
    context={
        'profile':profile,
        'posts':posts
    }
    return render(request,'a_profile/profile.html',context)

@login_required
def profile_edit_view(request):
    form=ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form=ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('a_profile')
    return render(request,'a_profile/profile_edit.html',{'form':form})

@login_required
def profile_delete_view(request):
    user=request.user
    if request.method=='POST':
        logout(request)
        user.delete()
        messages.success(request,'Account deleted, What a pity')
        return redirect('home')
    return render(request,'a_profile/profile_delete.html')

def profile_login(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['pswd']
        print(username)
        print(password)
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Crendentials Invalid')
            return redirect('profile_signup')
    else:
        return render(request,'a_profile/signin.html')

def profile_signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        pswd=request.POST['pswd']
        pswd2=request.POST['pswd2']

        if pswd ==pswd2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('profile_signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'UserName Taken')
                return redirect('profile_signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=pswd)
                user.save()
                print('raja1')
                # log user in and redirect to settings page 
                # create a Profile object for new user 
                user=User.objects.get(username=username)
                print('raja2')
                new_profile=Profile.objects.get_or_create(user=user)
                print('raja3')
                
                print('raja4')
                return redirect('profile_singin')

        else:
            messages.info(request,'Pasword is not same')
            return redirect('profile_signup')
     
    else:
        return render(request,'a_profile/signup.html')

def profile_logout(request):
    return render(request,'a_profile/profile_logout.html')