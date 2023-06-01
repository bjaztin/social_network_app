from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from helloYouApp.models import Profile, Relationship, Post

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'first_name',
            'last_name',
            'user',
            'about',
            'profile_pic',
            'friends',
        ]


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = [
            'id',
            'sender',
            'receiver',
            'status',
        ]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'status',
            'image_post',
            'author',
            'created',
        ]

