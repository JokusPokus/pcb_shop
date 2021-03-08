from django.db import models
from django.contrib.auth.models import User
import article.board_options as board_opt

from article.board_options import MIN_DIM_X, MAX_DIM_X, MIN_DIM_Y, MAX_DIM_Y


# Let's set a default category (which we could call "Misc", for example)
# that products can fall back to in the unlikely event that we delete a category.
DEFAULT_CATEGORY = 1


class Article(models.model):

    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(ArticleCategory, default=DEFAULT_CATEGORY, on_delete=models.SET_DEFAULT)

    class Meta:
        ordering = ['created']


class ArticleCategory(models.model):

    articleCategoryID = models.PositiveIntegerField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)


class Board(models.model):

    created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='boards', on_delete=models.CASCADE)

    gerberFileName = models.CharField(max_length=100)
    gerberHash = models.CharField(max_length=100)
    dimensionX = models.FloatField(validators=[MinValueValidator(MIN_DIM_X), MaxValueValidator(MAX_DIM_X)])
    dimensionY = models.FloatField(validators=[MinValueValidator(MIN_DIM_Y), MaxValueValidator(MAX_DIM_Y)])

    class Meta:
        ordering = ['created']
