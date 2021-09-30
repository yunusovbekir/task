from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import Car, Review


class CarSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source='make.title')
    model = serializers.CharField(source='model.title')

    class Meta:
        model = Car
        fields = (
            'id',
            'make',
            'model',
            'avg_rating',
        )


class PopularCarSerializer(CarSerializer):
    rates_number = serializers.IntegerField()

    class Meta:
        model = Car
        fields = (
            'id',
            'make',
            'model',
            'rates_number',
        )


class CreateReviewSerializer(serializers.Serializer):
    car_id = serializers.IntegerField()
    rating = serializers.IntegerField()

    def validate(self, attrs):
        """ Validate give car ID and rating. """

        rating = attrs.get('rating')
        car_id = attrs.get('car_id')

        if not Car.objects.filter(id=car_id).exists():
            raise serializers.ValidationError({
                "car_id": _("No car found with given ID")
            })

        if not 0 < rating < 6:
            raise serializers.ValidationError({
                "rating": _("Rating must be between 1 and 5")
            })

        return attrs

    def create(self, validated_data):
        return Review.objects.create(
            car_id=validated_data.get('car_id'),
            rating=validated_data.get('rating'),
        )
