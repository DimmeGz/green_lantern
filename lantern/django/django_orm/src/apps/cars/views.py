from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.cars.models import Car


class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    paginate_by = 100

    def get_queryset(self):
        queryset = Car.objects.all()
        dealer = self.request.GET.get('dealer_id')
        if dealer is not None:
            return queryset.filter(dealer_id=dealer)
        else:
            return queryset


class CarView(DetailView):
    model = Car
    template_name = 'car.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
