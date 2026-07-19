from django.db import models
import django.db.models.signals
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(
        upload_to='profiles/',
        default='profiles/default.png'
    )

    cover_photo = models.ImageField(
        upload_to='covers/',
        default='covers/default_cover.jpg'
    )

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


@receiver(django.db.models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
