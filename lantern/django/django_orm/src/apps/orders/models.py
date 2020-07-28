from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Index
from django.utils.translation import gettext_lazy as _

# Create your models here.
from common.models import BaseDateAuditModel


class Order(BaseDateAuditModel):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_SOLD = 'sold'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_SOLD, "Sold"),
        (STATUS_CANCELED, "Canceled"),
    )

    car_name = models.ForeignKey(to='cars.Car', on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING, blank=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=64)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    message = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

        indexes = [
            Index(fields=['status', ])
        ]
