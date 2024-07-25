from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile 

@receiver(post_save, sender=User)
def update_profile_email(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance, email=instance.email)
    else:
        profile = Profile.objects.get(user=instance)
        profile.email = instance.email  # Update profile's email to match user's email
        profile.save()