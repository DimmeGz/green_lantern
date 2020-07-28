from django.db import models
from django.db.models import Index, UniqueConstraint
from django.utils.translation import gettext_lazy as _

from apps.cars.managers import CarManager, CarQuerySet
from common.models import BaseDateAuditModel


class Color(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        indexes = [
            Index(fields=('name',))
        ]

        verbose_name = _('Color')
        verbose_name_plural = _('Colors')

    def __str__(self):
        return self.name


class CarBrand(models.Model):
    name = models.CharField(max_length=32, unique=True)
    logo = models.ImageField(null=True, blank=False)

    class Meta:
        ordering = ('name',)
        indexes = [
            Index(fields=('name',))
        ]
        verbose_name = _('Car brand')
        verbose_name_plural = _('Car brands')

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=64)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        indexes = [
            Index(fields=('name',)),
        ]
        verbose_name = _('Car model')
        verbose_name_plural = _('Car models')

    def __str__(self):
        return self.name


class CarEngine(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            Index(fields=('name',))
        ]
        verbose_name = _('Engine Type')
        verbose_name_plural = _('Engine Types')

    def __str__(self):
        return self.name


class FuelType(models.Model):
    name = models.CharField(max_length=12, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Fuel Type')
        verbose_name_plural = _('Fuel Types')

    def __str__(self):
        return self.name


class Car(BaseDateAuditModel):
    STATUS_PENDING = 'pending'
    STATUS_PUBLISHED = 'published'
    STATUS_SOLD = 'sold'
    STATUS_ARCHIVED = 'archived'

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_PUBLISHED, "Published"),
        (STATUS_SOLD, "Sold"),
        (STATUS_ARCHIVED, "Archived"),
    )

    objects = CarManager.from_queryset(CarQuerySet)()
    views = models.PositiveIntegerField(default=0, editable=False)
    slug = models.SlugField(max_length=75)
    number = models.CharField(max_length=16, unique=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING, blank=True)
    dealer = models.ForeignKey('dealers.Dealer', on_delete=models.CASCADE, related_name='cars', null=True, blank=False)
    color = models.ForeignKey(to='Color', on_delete=models.SET_NULL, null=True, blank=False)
    model = models.ForeignKey(to='CarModel', on_delete=models.SET_NULL, null=True, blank=False)
    extra_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Title second part'))

    engine_type = models.ForeignKey(to='CarEngine', on_delete=models.SET_NULL, null=True, blank=False)
    fuel_type = models.ForeignKey(to='FuelType', on_delete=models.SET_NULL, null=True, blank=False)
    engine_power = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=False)
    doors = models.PositiveSmallIntegerField(default=4)
    sitting_places = models.PositiveSmallIntegerField(default=4)
    first_registration_date = models.DateField(auto_now_add=False, null=True, blank=False)

    # other fields ...
    #

    def save(self, *args, **kwargs):
        order_number_start = 7600000
        if not self.pk:
            super().save(*args, **kwargs)
            self.number = f"LK{order_number_start + self.pk}"
            self.save()
        else:
            super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.status = self.STATUS_ARCHIVED
        self.save()

    @property
    def title(self):
        return f'{self.model.brand} {self.extra_title or ""}'  # do not show None

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

        indexes = [
            Index(fields=['status', ])
        ]


class Property(models.Model):
    category = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)


class CarProperty(models.Model):
    property = models.ForeignKey(to='Property', on_delete=models.DO_NOTHING, null=True, blank=False)
    car = models.ForeignKey(to='Car', on_delete=models.DO_NOTHING, null=True, blank=False)
