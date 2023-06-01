from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Forum, Message

@login_required
def forums(request):
    forums = Forum.objects.all()

    return render(request, 'forum/forums.html', {'forums': forums})

@login_required
def forum(request, slug):
    forum = Forum.objects.get(slug=slug)
    messages = Message.objects.filter(forum=forum)[0:25]

    return render(request, 'forum/forum.html', {'forum': forum, 'messages': messages})