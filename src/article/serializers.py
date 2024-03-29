from django.core.validators import ValidationError
from rest_framework import serializers

from .models import Board, Article, OfferedBoardOptions
from .validators import AttributeValidator


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.email", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)

    def validate_attributes(self, data) -> None:
        validator = AttributeValidator()
        try:
            validator.validate(data)
        except ValidationError as e:
            raise serializers.ValidationError("Not all chosen attributes are currently available:", e)
        return data

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ["gerberFileName", "gerberHash"]


class OfferedBoardOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferedBoardOptions
        fields = ["attribute_options"]
