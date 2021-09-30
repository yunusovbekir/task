from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Car, Review
from .serializers import (
    CarSerializer,
    PopularCarSerializer,
    CreateReviewSerializer,
)


class CarsListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class PopularCarsListAPIView(ListAPIView):
    queryset = Car.objects.annotate(rate=Count('reviews')).order_by('-rate')
    serializer_class = PopularCarSerializer


class CreateReviewAPIView(APIView):
    queryset = Review.objects.all()
    serializer_class = CreateReviewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
