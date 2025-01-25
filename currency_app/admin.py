from django.contrib import admin

from currency_app.models import CurrencyExchange, CountryTimeModel, Game

admin.site.register(CurrencyExchange)
admin.site.register(CountryTimeModel)
admin.site.register(Game)
