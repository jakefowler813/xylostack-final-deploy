"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from core.views import home, dashboard, delete_stack, add_stack, edit_stack, song_list, song_detail_api, play_song, help_page, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # Handles login/signup
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/delete/<int:stack_id>/', delete_stack, name='delete_stack'),
    path('dashboard/new/', add_stack, name='add_stack'),
    path('dashboard/edit/<int:stack_id>/', edit_stack, name='edit_stack'),
    path('songs/', song_list, name='song_list'),
    path('api/songs/<int:song_id>/', song_detail_api, name='song_detail_api'),
    path('play/<int:song_id>/<int:stack_id>/', play_song, name='play_song'),
    path('help/', help_page, name='help_page'),
    path('profile/', profile, name='profile'),
]