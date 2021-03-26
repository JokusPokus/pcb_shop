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
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = (
            'owner',
        )
