from rest_framework import serializers
from .models import Board, Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'created',
            'category'
        )


class BoardSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = Board
        fields = (
            'owner',
            'created',
            'category',
            'dimensionX',
            'dimensionY',
        )
