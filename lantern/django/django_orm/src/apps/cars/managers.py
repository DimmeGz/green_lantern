from django.db import models
from django.db.models.functions import Concat


class CarQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='published')

    def archived(self):
        return self.filter(status='archived')


class CarManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('model', 'model__brand')\
        #     .annotate(
        #     model_brand_title=Concat()
        # )
