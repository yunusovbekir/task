from django.urls import path
from .views import (
    CarsListAPIView,
    PopularCarsListAPIView,
    CreateReviewAPIView,
    DeleteCarAPIView,
)

urlpatterns = [
    path('cars/', CarsListAPIView.as_view(), name='cars'),
    path('popular/', PopularCarsListAPIView.as_view(), name='popular-cars'),
    path('delete/<int:id>/', DeleteCarAPIView.as_view(), name='delete'),
    path('rate/', CreateReviewAPIView.as_view(), name='rate'),
]
