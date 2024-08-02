from django.urls import path
from . import views


urlpatterns = [
    
    path('profile/',views.profile_view,name='a_profile'),
    path('<username>/',views.profile_view,name='userprofile'),
    path('profile/edit',views.profile_edit_view,name='a_profil_edit'),
    path('profile/delete',views.profile_delete_view,name='a_profil_delete'),
]
