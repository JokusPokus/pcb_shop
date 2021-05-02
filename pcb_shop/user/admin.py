from django.contrib import admin

from .models import BasketItem
from .address_management import Address


admin.site.register(BasketItem)
admin.site.register(Address)
