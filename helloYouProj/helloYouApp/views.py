from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .forms import ProfileForm, PostForm, UserForm
from django.contrib.auth.models import User
from .models import Profile, Post,  ProfileManager, UserRelationshipManager, Relationship

from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
        
            user = authenticate(username=username, password=password)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form':form})

@login_required()
def search_users(request):
    if request.method == "POST":
        searched = request.POST['searched']
        profiles = Profile.objects.filter(first_name__contains=searched)
        return render(request, 'main/search_users.html', {'searched': searched, 'profiles': profiles})
    else:
        return render(request, 'main/search_users.html', {})

@login_required
def view_posts(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    post_form = PostForm(request.POST or None, request.FILES or None)
    post_added = False
    
    profile = Profile.objects.get(user=request.user)

    if post_form.is_valid():
        instance = post_form.save(commit=False)
        instance.author = profile
        instance.save()
        post_form = PostForm()
        post_added = True
       
    context = {
        "posts": posts,
        "profile": profile,
        "post_form": post_form,
        "post_added": post_added,
    }
    return render(request, 'main/posts.html', context)

@login_required
def myProfile(request):
    userProfile = Profile.objects.get(user=request.user)
    all_posts = Post.objects.filter(author=userProfile)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=userProfile)
    confirm = False
    
    posts = Post.objects.all()
    post_form = PostForm(request.POST or None, request.FILES or None)
    post_added = False
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    if post_form.is_valid():
        instance = post_form.save(commit=False)
        instance.author = userProfile
        instance.save()
        post_form = PostForm()
        post_added = True
   
    context = {
        "userProfile": userProfile,
        "form": form,
        'all_posts':all_posts,
        "confirm": confirm,
        "posts": posts,
        "post_form": post_form,
        "post_added": post_added,
    }
    return render(request, 'main/myProfile.html', context)

@login_required
def invite_profiles_list_view(request):
    user = request.user
    query_set = Profile.objects.show_all_profiles_to_invite(user)

    context = {'query_set': query_set}

    return render(request, 'main/invite_list.html', context)

@login_required
def profiles_list_view(request):
    user = request.user
    query_set = Profile.objects.show_all_profiles(user)

    context = {'query_set': query_set}

    return render(request, 'main/all_profiles.html', context)

@login_required
def viewProfile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    all_posts = Post.objects.filter(author=profile)

    context = {
    "user": user,
    "profile": profile,
    "all_posts": all_posts,
    }
    return render(request, 'main/viewProfile.html', context)
    
class ProfileListView(ListView):
    model = Profile
    template_name = 'main/all_profiles.html'

    def get_queryset(self):
        query_set = Profile.objects.show_all_profiles(self.request.user)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context

@login_required
def view_invites(request):
    profile = Profile.objects.get(user=request.user)
    invitation = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, invitation))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'invitation': results,
        'is_empty': is_empty,
    }

    return render(request, 'main/myInvitations.html', context)

@login_required
def send_invite(request):
     if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
        return redirect('helloYouApp:myProfile')

@login_required
def accept_invite(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accept'
            rel.save()
    return redirect('view_invites')

@login_required
def reject_invite(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect ('view_invites')

@login_required
def unfriend(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('helloYouApp:myProfile')