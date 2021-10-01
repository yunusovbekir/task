from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review


@receiver(post_save, sender=Review, dispatch_uid="calculate_rating")
def calculate_rating(instance, created, **kwargs):
    getattr(instance.car, 'update_rating')()
