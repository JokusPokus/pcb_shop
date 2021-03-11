from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from article.board_options import OPTIONS


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
        ordering = ['created']


class Board(models.Model):
    """Model for PCBs"""
    created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User,
        related_name='boards',
        on_delete=models.CASCADE
    )

    # We probably have to refine this
    gerberFileName = models.CharField(max_length=100)
    gerberHash = models.CharField(max_length=100)

    # *************
    # Board options
    # *************

    dimensionX = models.FloatField(validators=[MinValueValidator(0)])
    dimensionY = models.FloatField(validators=[MinValueValidator(0)])
    differentDesigns = models.PositiveIntegerField()
    layers = models.PositiveIntegerField()
    deliveryFormat = models.CharField(max_length=30)
    thickness = models.FloatField()
    color = models.CharField(max_length=30)
    surfaceFinish = models.CharField(max_length=30)
    copperWeight = models.PositiveIntegerField()
    goldFingers = models.CharField(max_length=30)
    castellatedHoles = models.CharField(max_length=30)
    removeOrderNum = models.CharField(max_length=30)
    confirmProdFile = models.CharField(max_length=30)
    flyingProbeTest = models.CharField(max_length=30)

    class Meta:
        ordering = ['created']
