from rest_framework.viewsets import ModelViewSet

from helloYouApp.models import Profile, Relationship, Post 
from helloYouApp.api.serializers import ProfileSerializer, RelationshipSerializer, PostSerializer

class ProfileViewset(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class RelationshipViewset(ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer

class PostViewset(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
