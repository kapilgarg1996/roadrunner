from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth.models import User

from mysite.profiles.models import UserProfile


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
