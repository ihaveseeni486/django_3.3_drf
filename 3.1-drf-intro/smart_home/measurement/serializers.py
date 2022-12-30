from rest_framework import serializers
from .models import Measurement, Sensor


class MeasurementShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        # fields = '__all__'
        fields = ['temperature', 'created_at']
        extra_kwargs = {
            'sensor_id': {
                'write_only': True
            }
        }


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'


class SensorShortDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        # fields = '__all__'
        fields = ['id', 'name', 'description']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementShortSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']

