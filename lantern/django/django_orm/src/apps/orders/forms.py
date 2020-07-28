from apps.orders.models import Order
from django.forms import models


class OrderForm(models.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
