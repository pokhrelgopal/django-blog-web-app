from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginuser, name='login'),
    path('register/', views.registeruser, name='register'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('posts/', views.posts, name='posts'),
    path('add-post/', views.addPost, name='add-post'),
    path('single-post/<str:pk>/', views.singlePost, name='single-post'),
    path('profile-blog/', views.profileBlog, name='profile-blog'),

    path('delete-post/', views.deletePost, name='delete-post'),
    path('edit-post/<str:pk>/', views.editPost, name='edit-post'),

    path('update-profile/', views.updateProfile, name='update-profile'),

]