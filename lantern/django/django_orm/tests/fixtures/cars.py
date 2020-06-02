from uuid import uuid4

import factory

from apps.cars.models import Car, CarBrand, CarModel


class CarBrandFactory(factory.DjangoModelFactory):
    logo = factory.django.ImageField(color='blue')

    class Meta:
        model = CarBrand


class CarModelFactory(factory.DjangoModelFactory):
    brand = factory.SubFactory(CarBrandFactory)
    name = factory.LazyFunction(lambda: uuid4().hex)

    class Meta:
        model = CarModel


class CarFactory(factory.DjangoModelFactory):
    model = factory.SubFactory(CarModelFactory)

    class Meta:
        model = Car
