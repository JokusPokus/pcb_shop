from django.db import models
from django.contrib.auth.models import User

# Let's set a default category ("Misc", for example)
# that products can fall back to in the unlikely event that we delete a category.
DEFAULT_CATEGORY = 1


class ArticleCategory(models.Model):
    """Model for article categories, such as PCBs."""
    articleCategoryID = models.PositiveIntegerField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)


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


class ExternalShop(models.Model):
    """Model for external PCB shop."""
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)


class OfferedBoardOptions(models.Model):
    """Model to store the board options offered by the PCB shop at any given time."""
    created = models.DateTimeField(auto_now_add=True)
    attribute_options = models.JSONField()

    class Meta:
        ordering = ['-created']


class ExternalBoardOptions(models.Model):
    """Model to store the board options externally available in some PCB shop at any given time."""
    created = models.DateTimeField(auto_now_add=True)
    external_shop = models.ForeignKey(ExternalShop, on_delete=models.DO_NOTHING)
    attribute_options = models.JSONField()

    class Meta:
        ordering = ['-created']
