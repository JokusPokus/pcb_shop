from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.apps import apps
from django.db.models.signals import post_save

from auditlog.registry import auditlog

from article.validators import validate_external_consistency

# Let's set a default category ("Misc", for example)
# that products can fall back to in the unlikely event that we delete a category.
DEFAULT_CATEGORY = 1


class ArticleCategory(models.Model):
    """Model for article categories, such as PCBs."""
    articleCategoryID = models.PositiveIntegerField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)

    class Meta:
        verbose_name = "Article Category"
        verbose_name_plural = "Article Categories"

    def __str__(self):
        return f"<ArticleCategory: {self.name}>"


class Article(models.Model):
    """Model for any article sold in the shop,
    including - but not constrained to - PCBs.
    """
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        ArticleCategory,
        default=DEFAULT_CATEGORY,
        on_delete=models.SET_DEFAULT
    )

    class Meta:
        ordering = ['-created']


class Board(Article):
    """Model for PCBs"""
    owner = models.ForeignKey(
        User,
        related_name='boards',
        on_delete=models.CASCADE
    )

    # We probably have to refine this
    gerberFileName = models.CharField(max_length=100)
    gerberHash = models.CharField(max_length=100)

    attributes = models.JSONField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"<Board by user {self.owner.email}>"


@receiver(post_save, sender=Board)
def create_basket_item(sender, instance, created, **kwargs):
    """Ensures that a created Board is automatically stored
    in the user's basket.
    """
    if created:
        BasketItem = apps.get_model("user", "BasketItem")
        BasketItem.objects.create(article=instance, owner=instance.owner)


class ExternalShop(models.Model):
    """Model for external PCB shop."""
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Eternal Shop"

    def __str__(self):
        return f"<ExternalShop: {self.name}>"


class OfferedBoardOptions(models.Model):
    """Model to store the board options offered by the PCB shop at any given time."""
    created = models.DateTimeField(auto_now_add=True)
    attribute_options = models.JSONField(validators=[validate_external_consistency])

    class Meta:
        ordering = ['-created']
        verbose_name = "Offered Board Options"
        verbose_name_plural = "Offered Board Options List"

    def __str__(self):
        return f"<OfferedBoardOptions created at {self.created}>"


class ExternalBoardOptions(models.Model):
    """Model to store the board options externally available in some PCB shop at any given time."""
    created = models.DateTimeField(auto_now_add=True)
    external_shop = models.ForeignKey(ExternalShop, on_delete=models.DO_NOTHING)
    attribute_options = models.JSONField()

    class Meta:
        ordering = ['-created']
        verbose_name = "External Board Options"
        verbose_name_plural = "External Board Options List"

    def __str__(self):
        return f"<ExternalBoardOptions from shop '{self.external_shop.name}'>"


auditlog.register(ArticleCategory)
auditlog.register(Article)
auditlog.register(Board)
auditlog.register(ExternalShop)
auditlog.register(OfferedBoardOptions)
auditlog.register(ExternalBoardOptions)
