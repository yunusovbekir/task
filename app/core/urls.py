from django.urls import path
from .views import CarsListAPIView, PopularCarsListAPIView

urlpatterns = [
    path('cars/', CarsListAPIView.as_view(), name='cars'),
    path('popular/', PopularCarsListAPIView.as_view(), name='popular-cars'),
]
