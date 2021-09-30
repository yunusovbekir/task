from rest_framework import serializers
from .models import Car


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
