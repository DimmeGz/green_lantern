from django.forms import ModelForm

from apps.photos.models import Photo


class AddImageForm(ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'
