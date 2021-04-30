from django.contrib import admin

from user.models import BasketItem
from user.address_management import Address


admin.site.register(BasketItem)
admin.site.register(Address)
