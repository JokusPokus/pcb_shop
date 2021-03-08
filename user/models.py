from django.db import models
# from article.models import Article


class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=254)
    defaultShippingAddressID = models.IntegerField()
    defaultBillingAddressID = models.IntegerField()

    class Meta:
        ordering = ['created']


class BasketItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
