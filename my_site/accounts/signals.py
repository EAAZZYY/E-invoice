from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile


"""
Logic to create a user profile once a user instance has been created
"""

@receiver(post_save,sender=User)
def build_profile(sender,created,instance,**kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)        
def save_profile(sender,instance,**kwargs):
    instance.profile.save()