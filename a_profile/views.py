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

def prfile_login(request):
    return render(request,'a_profile/profile_login.html')

def prfile_signup(request):
    return render(request,'a_profile/profile_signup.html')

def prfile_logout(request):
    return render(request,'a_profile/profile_logout.html')