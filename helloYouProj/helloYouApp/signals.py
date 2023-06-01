from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Relationship)
def post_save_add_friends(sender, instance, created, **kwargs):
    user_sender = instance.sender
    user_receiver = instance.receiver
    if instance.status == 'accept':
        user_sender.friends.add(user_receiver.user)
        user_receiver.friends.add(user_sender.user)
        user_sender.save()
        user_receiver.save()

@receiver(pre_delete, sender=Relationship)
def pre_delete_unfriend(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()

