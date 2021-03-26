from rest_framework import serializers
from .models import Board, Article


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.email', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Board
        fields = '__all__'
