from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from auditlog.registry import auditlog

from article.models import Article
from user.address_management import Address


# **********
# BASKET
# **********

class BasketItem(models.Model):
    """Model for articles that are contained in a user's basket."""
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['created']
        unique_together = ['owner', 'article']


auditlog.register(User)
auditlog.register(BasketItem)
