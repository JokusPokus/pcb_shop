from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# from article.models import Article
from user.address_management import Address


# **********
# USERS
# **********

# We want to use Django's user model for authentication, but we
# need to store more information.
# The solution is presented here:
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone


class Profile(models.Model):

    # OneToOneField makes Profile an "extension" of the in-built User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=254)
    defaultShippingAddress = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    defaultBillingAddress = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['created']


# We are hooking the create_user_profile and save_user_profile methods
# to the User model, whenever a save event occurs:

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
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
        unique_together = ['user', 'article']
