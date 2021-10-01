from django.db import models


class CustomManager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        super().bulk_create(objs, **kwargs)
        for obj in objs:
            getattr(obj.car, 'update_rating')()
