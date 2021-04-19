from django.contrib import admin
from django.core.exceptions import ValidationError
from article.models import (
    Article,
    ArticleCategory,
    Board,
    ExternalShop,
    ExternalBoardOptions,
    OfferedBoardOptions
)
from article.validators import BoardOptionValidator


admin.site.register(Article)
admin.site.register(ArticleCategory)
admin.site.register(Board)
admin.site.register(ExternalShop)
admin.site.register(ExternalBoardOptions)
admin.site.register(OfferedBoardOptions)
