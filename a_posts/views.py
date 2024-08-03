from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.forms import ModelForm
from django.http import HttpResponse
from .models import*
from .forms import *
from django import forms
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.




def home_view(request,tag=None):
    if tag:
        posts=Post.objects.filter(tags__slug=tag)
        tag=get_object_or_404(Tag, slug=tag)
    else:
        posts=Post.objects.order_by("?")
    paginator = Paginator(posts, 3)
    page = int(request.GET.get('page', 1))
    try:
        posts = paginator.page(page)
    except:
        return HttpResponse('')

    # try:
    #     feature_herobutton = feature_enabled(1, 'Andreas')
    # except:
    #     feature_herobutton = False
    context={
        'posts':posts,
        'tag':tag,
        'page':page
    }

    if request.htmx:
        return render(request, 'a_posts/loop_home_posts.html', context)
    return render(request,'a_posts/home.html',context)
    
    


@login_required
def post_create_view(request):
    form=PostCreateForm()
    if request.method == 'POST':
        form=PostCreateForm(request.POST,request.FILES)
        for i in form:
            print(i)
        if form.is_valid():
            form.save()
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('home')
    return render(request,'a_posts/posts_create.html',{'form':form})

@login_required
def post_delete_view(request,pk):
    post=get_object_or_404(Post, id=pk, author=request.user)
    if request.method=='POST':
        post.delete()
        messages.success(request,'post deleted')
        return redirect('home')
    return render(request,'a_posts/post_delete.html',{'post':post})


@login_required
def post_edit_view(request,pk):
    post=get_object_or_404(Post,id=pk,author=request.user)
    form=PostEditForm(instance=post)
    if request.method=='POST':
        form=PostEditForm(request.POST,request.FILES,instance=post)
        if form.is_valid:
            form.save()
            # instance = form.save(commit=False)
            # instance.author = request.user
            # instance.save()
            # form.save_m2m()
            messages.success(request,'post updated')
            return redirect('home')
    context={
        'post':post,
        'form':form
    }
    
    return render(request,'a_posts/post_edit.html',context)


    # return render(request,'a_posts/posts_delete.html')

def post_page_view(request,pk):
    post=get_object_or_404(Post,id=pk)
    commentform=CommentCreateForm()
    replyform=ReplyCreateForm()
    categories=Tag.objects.all()

    if request.htmx:
        if 'top' in request.GET:
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        return render(request,'a_posts/loop_postpage_comments.html',{'comments':comments,'replyform':replyform})

    context={
        'post':post,
        'commentform':commentform,
        'replyform':replyform,
        'categories':categories
    }
    return render(request,'a_posts/post_page.html',context)

@login_required
def comment_sent(request,pk):
    post = get_object_or_404(Post, id=pk)
    replyform = ReplyCreateForm()
    
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post            
            comment.save()
            
    context = {
        'post' : post,
        'comment': comment,
        'replyform': replyform
    }

    return render(request,'a_posts/add_comment.html',context)


@login_required
def reply_sent(request,pk):
    comment=get_object_or_404(Comment,id=pk)
    replyform=ReplyCreateForm()
    if request.method=='POST':
        form=ReplyCreateForm(request.POST)
        if form.is_valid:
            reply=form.save(commit=False)
            reply.author=request.user
            reply.parent_comment=comment
            reply.save()

    context={
        'comment':comment,
        'reply':reply,
        'replyform':replyform
        }
    return render(request,'a_posts/add_reply.html',context)



@login_required
def comment_delete_view(request,pk):
    post=get_object_or_404(Comment, id=pk, author=request.user)
    if request.method=='POST':
        post.delete()
        messages.success(request,'comment deleted')
        return redirect('post',post.parent_post.id)
    return render(request,'a_posts/comment_delete.html',{'comment':post})



@login_required
def reply_delete_view(request,pk):
    reply=get_object_or_404(Reply, id=pk, author=request.user)
    if request.method=='POST':
        reply.delete()
        messages.success(request,'reply deleted')
        return redirect('post',reply.parent_comment.parent_post.id)
    return render(request,'a_posts/reply_delete.html',{'reply':reply})

def like_toggle(model):
    def inner_func(func):
        def wrapper(request,*args,**kwargs):
            post=get_object_or_404(model,id=kwargs.get('pk'))
            user_exist=post.likes.filter(username=request.user.username).exists()
            if post.author !=request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)
            return func(request,post)
        return wrapper
    return inner_func


@login_required
@like_toggle(Post)
def like_post(request,post):
    return render(request,'a_posts/likes.html',{'post':post})

@login_required
@like_toggle(Comment)
def like_comment(request,Post):
    return render(request,'a_posts/likes_comment.html',{'comment':Post})

@login_required
@like_toggle(Reply)
def like_reply(request,Post):
    return render(request,'a_posts/likes_reply.html',{'reply':Post})