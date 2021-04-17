from django.contrib import admin

from article.models import (
    Article,
    ArticleCategory,
    Board,
    ExternalShop,
    ExternalBoardOptions,
    OfferedBoardOptions
)

admin.site.register(Article)
admin.site.register(ArticleCategory)
admin.site.register(Board)
admin.site.register(ExternalShop)
admin.site.register(ExternalBoardOptions)
admin.site.register(OfferedBoardOptions)
