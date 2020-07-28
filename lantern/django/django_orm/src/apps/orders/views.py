from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy

from apps.orders.forms import OrderForm
from apps.orders.models import Order
from django.views.generic import FormView, ListView


class OrderView(FormView):
    model = Order
    form_class = OrderForm
    template_name = 'order_page.html'
    success_url = reverse_lazy("order_list")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def order_add(request):
        return render(request, 'orders/orders.html', {})


class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'
    paginate_by = 100

    def get_queryset(self):
        queryset = Order.objects.all()
        dealer = self.request.GET.get('dealer_id')
        if dealer is not None:
            return queryset.filter(dealer_id=dealer)
        else:
            return queryset
