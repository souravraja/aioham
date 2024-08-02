from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name='home'),
    path('category/<tag>/',views.home_view,name='category'),
    path('create/',views.post_create_view,name='post-create'),
    path('delete/<pk>',views.post_delete_view,name='post-delete'),
    path('edit/<pk>',views.post_edit_view,name='post-edit'),
    path('post/<pk>',views.post_page_view,name='post'),
    path('post/<pk>/like/',views.like_post,name='like-post'),
    path('post/like/<pk>/',views.like_comment,name='like-comment'),
    path('reply/like/<pk>/',views.like_reply,name='like-reply'),
    path('commentsent/<pk>',views.comment_sent,name='comment-sent'),
    path('commentdelete/<pk>',views.comment_delete_view,name='comment-delete'),
    path('reply-sent/<pk>',views.reply_sent,name='reply-sent'),
    path('reply-delete/<pk>',views.reply_delete_view,name='reply-delete'),
 
]
