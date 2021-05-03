from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = [
            "order_state",
            "payment_state",
            "user",
            "value",
            "vat",
            "amount",
            "shipping_cost",
            "items"
        ]
