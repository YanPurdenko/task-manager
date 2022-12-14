from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile
from app.models import Worker


@receiver(post_save, sender=Worker)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(worker=instance)


@receiver(post_save, sender=Worker)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
