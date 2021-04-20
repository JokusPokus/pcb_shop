from rest_framework import serializers
from .models import Board, Article, OfferedBoardOptions


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.email", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)

    def validate_attributes(self):
        pass

    class Meta:
        model = Board
        fields = "__all__"


class OfferedBoardOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferedBoardOptions
        fields = ["attribute_options"]
