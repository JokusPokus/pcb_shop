from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from article.models import Article
from user.address_management import Address


# **********
# USERS
# **********

class Profile(models.Model):
    """Extends the inbuilt User model to add more information about a User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Ensures that a User Profile is created together with
    a new User.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Ensures that a User's Profile is updated in the event
    of a User update.
    """
    instance.profile.save()


# **********
# BASKET
# **********

class BasketItem(models.Model):
    """Model for articles that are contained in a user's basket."""
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
        unique_together = ['owner', 'article']
