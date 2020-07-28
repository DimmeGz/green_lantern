from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=56, unique=True)
    code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class City(models.Model):
    name = models.CharField(max_length=85, unique=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class Dealer(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
