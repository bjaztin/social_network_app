"""helloYouProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from helloYouApp.api import viewsets, views
from .views import (myProfile, 
view_posts, 
ProfileListView, 
profiles_list_view, 
invite_profiles_list_view,
send_invite,
unfriend,
accept_invite,
reject_invite,
viewProfile,
register,
search_users,
view_invites,)


schema_view = swagger_get_schema_view(
    openapi.Info(
        title='Post API',
        default_version='v1',
        description = 'API documentation of App',
    ),
    public=True,
    permission_classes =(permissions.AllowAny,)
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', register, name='register'),
    path('myProfile/', myProfile, name='myProfile'),
    path('posts/', view_posts, name='view_posts'),
    path('myInvitations/', view_invites, name='view_invites'),
    path('all_profiles/', ProfileListView.as_view(), name='view_all_profiles'),
    path('invite_list/', invite_profiles_list_view, name='invite_profiles_list_view'),
    path('send_invite/', send_invite, name='send_invite'),
    path('myInvitations/accept_invite/', accept_invite, name='accept_invite'),
    path('myInvitations/reject_invite/', reject_invite, name='reject_invite'),
    path('unfriend/', unfriend, name='unfriend'),
    path('<str:username>', viewProfile, name='viewProfile'),
    path('search_users/', search_users, name='search_users'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
