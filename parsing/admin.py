from django.contrib import admin

from parsing.models import TradingPlace, Bank, CryptoCurrency, Order


admin.site.register(TradingPlace)
admin.site.register(Bank)
admin.site.register(CryptoCurrency)
admin.site.register(Order)
