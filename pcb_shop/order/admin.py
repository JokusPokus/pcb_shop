from django.contrib import admin

from pcb_shop.order.models import Order, OrderState, PaymentState, Article2Order, ShippingMethod, ShippingProvider

admin.site.register(Order)
admin.site.register(OrderState)
admin.site.register(PaymentState)
admin.site.register(Article2Order)
admin.site.register(ShippingProvider)
admin.site.register(ShippingMethod)
