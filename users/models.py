import uuid
from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


def get_activation_key_expires():
    return now() + timedelta(hours=48)


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)

    activation_key = models.UUIDField(default=uuid.uuid4)
    activation_key_expires = models.DateTimeField(default=get_activation_key_expires)

    @property
    def is_activation_key_expired(self):
        return now() > self.activation_key_expires

    def activate(self):
        self.is_active = True
        self.activation_key_expires = now()

    def safe_delete(self):
        self.is_active = False
        self.save()


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    NON_BINARY = 'N'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NON_BINARY, 'Non binary'),
    ]

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    gender = models.CharField(User, max_length=1, choices=GENDER_CHOICES)
    about = models.TextField(User, blank=True)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = UserProfile(user=instance)
            profile.save()
