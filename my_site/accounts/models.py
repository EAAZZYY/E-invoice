from django.db import models

from django.conf import settings
from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.

"""
User Profile Model
"""
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=True, null=True)
    profile_pix = models.ImageField(upload_to="profile_pic",default="defaultimg.jpg", blank=True,null=True)
    created_on = models.DateTimeField(auto_now=True)
    edited_on = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    """
    method to save when profile is last edited
    """
    def save(self,*args,**kwargs):
        if self.edited_on == "None":
            self.edited_on = timezone.localtime(timezone.now)
        return super(Profile, self).save(*args,**kwargs)