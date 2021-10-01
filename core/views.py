from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Car, Review
from .serializers import (
    CarSerializer,
    PopularCarSerializer,
    CreateReviewSerializer,
    CreateCarSerializer,
)


class CarsAPIView(ListAPIView):
    """ API endpoint to list all cars and create a new car """

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    post_serializer_class = CreateCarSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.post_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class PopularCarsListAPIView(ListAPIView):
    """
        API endpoint to list all cars ordered by review count.
    """
    queryset = Car.objects.annotate(rate=Count('reviews')).order_by('-rate')
    serializer_class = PopularCarSerializer


class DeleteCarAPIView(APIView):
    """
        API endpoint to delete a car.
        If there isn't a car in db with given ID, return 404 error.
    """

    def delete(self, request, *args, **kwargs):
        car_id = kwargs.get('id')

        try:
            Car.objects.get(id=car_id).delete()
            return Response(status=204)
        except Car.DoesNotExist:
            return Response(
                {"error": _("No car found with given ID")}, status=404
            )


class CreateReviewAPIView(APIView):
    """ API endpoint to rate a car """

    queryset = Review.objects.all()
    serializer_class = CreateReviewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
