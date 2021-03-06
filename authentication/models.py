"""
Models keeps track of all the persistent data around the user profile
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Profile represents additional values for a user account
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    has_bank_linked = models.NullBooleanField(
        blank=True, default=False, null=True)

    def __str__(self):
        return "{}, {}, {}".format(self.id, self.user_id, self.has_bank_linked)


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **_):
    """
    Creates a linked profile when a user account is created
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(instance, **_):
    """
    To be safe, whenever the user profile is saved, we also save the profile
    """
    instance.profile.save()


class UserBank(models.Model):
    """
    Contains all the user's bank access data (via plaid)
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='userbank'
    )
    item_id = models.CharField(max_length=1000)
    access_token = models.CharField(max_length=1000)
    institution_name = models.CharField(max_length=1000)

    def __str__(self):
        return "IDs:{}, {}, Institution: {}. ".format(self.institution_name, self.id, self.user_id)
