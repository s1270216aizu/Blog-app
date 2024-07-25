"""
URL configuration for blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.main, name="view-main"),
    path("home", views.main,name = "home"),
    path("login_frame", views.login_frame),
    path("register_frame", views.register_frame),
    path("register_form_frame", views.register_form_frame),
    path("do_register", views.do_register),
    path("do_check_regform", views.do_check_regform),
    path("do_login", views.do_login),
    path("do_logout", views.do_logout,name='do_logout'),
    path("hello", views.hello),
    path('blogs/', views.blog_list_view, name='blog_list'),
    path('create/', views.create_blog_view, name='create_blog'),
    path('user_icon/', views.user_icon, name='user_icon'),
    path('create_button/', views.create_button, name='create_button'),
    path('delete_button/', views.delete_button, name='delete_button'),
    path('user_profile_button/', views.user_profile_button, name='user_profile_button'),
    path('author/<str:author_name>/', views.author_blog_list_view, name='author_blog_list'),
    path('register_userdata/', views.register_userdata, name='register'),
    path('delete_blogs/', views.delete_blogs_view, name='delete_blogs'),
    path('delete_selected/', views.delete_selected_blogs, name='delete_selected'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
