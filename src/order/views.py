from rest_framework import generics

from .serializers import OrderSerializer
from .models import Order, OrderState, PaymentState


class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        order_state = OrderState.objects.get(name="received")
        payment_state = PaymentState.objects.get(name="pending")
        user = self.request.user
        value = 15.99
        vat = 1.12
        serializer.save(
            order_state=order_state,
            payment_state=payment_state,
            user=user,
            value=value,
            vat=vat,
        )
