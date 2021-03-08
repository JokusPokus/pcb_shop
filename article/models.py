from django.db import models
from django.contrib.auth.models import User
import article.board_options as board_opt

from article.board_options import OPTIONS


# Let's set a default category (which we could call "Misc", for example)
# that products can fall back to in the unlikely event that we delete a category.
DEFAULT_CATEGORY = 1


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


class ArticleCategory(models.Model):
    """Model for article categories, such as PCBs."""

    articleCategoryID = models.PositiveIntegerField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)


class Board(models.Model):
    """Model for PCBs, based on constantly updated
    board option constraints.
    """

    @staticmethod
    def choice_args(option_name: str, options: dict = OPTIONS) -> dict:
        """Helper function to define model field parameters
        for categorical board options in a DRY way."""

        return {
            "choices": options[option_name]["choices"],
            "default": options[option_name]["default"]
        }

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

    dimensionX = models.FloatField(
        validators=[MinValueValidator(OPTIONS["dim_x"]["min"]),
                    MaxValueValidator(OPTIONS["dim_x"]["max"])]
    )
    dimensionY = models.FloatField(
        validators=[MinValueValidator(OPTIONS["dim_y"]["min"]),
                    MaxValueValidator(OPTIONS["dim_y"]["max"])]
    )
    differentDesigns = models.PositiveIntegerField(
        **choice_args("num_designs")
    )
    layers = models.PositiveIntegerField(
        **choice_args("layers")
    )
    deliveryFormat = models.CharField(
        max_length=30,
        **choice_args("delivery_format")
    )
    thickness = models.FloatField(
        **choice_args("thickness")
    )
    color = models.CharField(
        max_length=30,
        **choice_args("color")
    )
    surfaceFinish = models.CharField(
        max_length=30,
        **choice_args("surface_finish")
    )
    copperWeight = models.PositiveIntegerField(
        **choice_args("copper_weight")
    )
    goldFingers = models.CharField(
        max_length=30,
        **choice_args("gold_fingers")
    )
    castellatedHoles = models.CharField(
        max_length=30,
        **choice_args("castellated_holes")
    )
    removeOrderNum = models.CharField(
        max_length=30,
        **choice_args("remove_order_num")
    )
    confirmProdFile = models.CharField(
        max_length=30,
        **choice_args("confirm_prod_file")
    )
    flyingProbeTest = models.CharField(
        max_length=30,
        **choice_args("flying_probe_test")
    )

    class Meta:
        ordering = ['created']
