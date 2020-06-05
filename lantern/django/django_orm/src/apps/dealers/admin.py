from django.contrib import admin

# Register your models here.
from apps.dealers.models import Dealer, City, Country


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
