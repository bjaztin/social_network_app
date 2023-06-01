from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db.models import Q
from django.shortcuts import reverse
# Create your models here.

class ProfileManager(models.Manager):

    def show_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        invitation = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(invitation)
       

        accept = set([])
        for rel in invitation:
            if rel.status == 'accept':
                accept.add(rel.receiver)
                accept.add(rel.sender)
        print(accept)
     

        available = [profile for profile in profiles if profile not in accept]
        print(available)
        return available
        

    def show_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(default="Welcome to my profile!", max_length=300)
    profile_pic = models.ImageField(default='profile_pic.png', upload_to='profile_pics/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')


    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    def get_url(self):
        return reverse('viewProfile', kwargs={"username":self.user.username})

    def show_friends(self):
        return self.friends.all()

    def show_friends_number(self):
        return self.friends.all().count()
        print('hello')
    
    def show_posts_number(self):
        return self.posts.all().count()
    
    def __str__(self):
        return '{} - {}'.format(self.pk, self.user)
    

STATUS_CHOICES = (
    ('send', 'send'), ('accept', 'accept')
)

class UserRelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        invitations = Relationship.objects.filter(receiver=receiver, status='send')
        return invitations

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=6, choices=STATUS_CHOICES)

    objects = UserRelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

class Post(models.Model):
    status = models.TextField()
    image_post = models.ImageField(upload_to='posts', blank=True, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.status[:20])

    class Meta:
         ordering = ('-created',)