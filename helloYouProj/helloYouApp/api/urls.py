from django.urls import path, include
from rest_framework.routers import SimpleRouter

from helloYouApp.api import viewsets, views

router = SimpleRouter()
router.register(r'profile', viewsets.ProfileViewset, basename='profile')
router.register(r'relationship', viewsets.RelationshipViewset, basename='relationship')
router.register(r'post', viewsets.PostViewset, basename='post')

urlpatterns = [
    path('ping/', views.PingView.as_view(), name='ping'),
] + router.get_urls()
