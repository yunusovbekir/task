from requests import get
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework import serializers
from .models import Car, Review, Make, Model


VEHICLE_API = settings.VEHICLE_API


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


class CreateCarSerializer(serializers.Serializer):
    make = serializers.CharField()
    model = serializers.CharField()
    error_message = _("No car found with given data")

    def validate(self, attrs):
        attrs = super().validate(attrs)

        make = attrs.get('make')
        model = attrs.get('model')

        self.validate_car(make, model)

        return attrs

    def validate_car(self, make, model):
        """ Check if there's an actual car with given data """

        api_url = VEHICLE_API + f'{make}?format=json'
        data = get(api_url).json()

        # if count is 0, there's no car with given make
        if data.get('Count') == 0:
            raise serializers.ValidationError({"make": self.error_message})

        # else we should check if there's a model with given model title
        models = data.get('Results')
        for model_dict in models:
            if model_dict.get('Model_Name') == model:
                return  # if found, break the flow

        # else raise exception with user-friendly error message
        raise serializers.ValidationError({"model": self.error_message})

    def create(self, validated_data):
        make = validated_data.get('make')
        model = validated_data.get('model')

        make_obj, _ = Make.objects.get_or_create(title=make)
        model_obj, _ = Model.objects.get_or_create(make=make_obj, title=model)
        car, _ = Car.objects.get_or_create(make=make_obj, model=model_obj)

        return car


class CreateReviewSerializer(serializers.Serializer):
    car_id = serializers.IntegerField()
    rating = serializers.IntegerField()

    def validate(self, attrs):
        """ Validate give car ID and rating. """
        attrs = super().validate(attrs)

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
