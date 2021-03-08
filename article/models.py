from django.db import models


# Let's set a default category (which we could call "Misc", for example)
# that products can fall back to in the unlikely event that we delete a category.
DEFAULT_CATEGORY = 1


class Article(models.model):

    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(ArticleCategory, default=DEFAULT_CATEGORY, on_delete=models.SET_DEFAULT)

    class Meta:
        ordering = ['created']


