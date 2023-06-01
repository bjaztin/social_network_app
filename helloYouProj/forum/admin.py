from django.contrib import admin

from .models import Forum, Message

admin.site.register(Forum)
admin.site.register(Message)