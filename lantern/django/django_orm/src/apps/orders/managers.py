from django.db import models


class OrderQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(status='pending')

    def paid(self):
        return self.filter(status='paid')

    def sold(self):
        return self.filter(status='sold')

    def canceled(self):
        return self.filter(status='canceled')

