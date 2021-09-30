from django.db.models import Count
from rest_framework.generics import ListAPIView
from .models import Car
from .serializers import CarSerializer, PopularCarSerializer


class CarsListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class PopularCarsListAPIView(ListAPIView):
    queryset = Car.objects.annotate(rate=Count('reviews')).order_by('-rate')
    serializer_class = PopularCarSerializer
