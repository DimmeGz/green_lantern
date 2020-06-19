from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from apps.photos.models import Photo
from apps.photos.forms import AddImageForm


class UpdateImageView(FormView):
    model = Photo
    form_class = AddImageForm
    template_name = 'update_photo.html'
    success_url = reverse_lazy("car_list")

    def get_success_url(self):
        return reverse('car_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
