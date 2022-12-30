# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
# from rest_framework.response import Response

from .models import Sensor, Measurement
from .serializers import SensorDetailSerializer, SensorShortDetailSerializer, MeasurementSerializer


# список сенсоров с краткой информацией и создание
class SensorsView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorShortDetailSerializer

    # def post(self, request):
    #     try:
    #         name = request.data.get('name')
    #         description = request.data.get('description', '')
    #         Sensor(
    #             name=name,
    #             description=description
    #             ).save()
    #         return Response({'status': 'ok'})
    #     except Exception as e:
    #         return Response({'status': 'error', 'exception': f'{e}'})


# получить информацию по датчику и изменить датчик
class SensorView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

# добавление измерения
# class MeasurementsView(ListCreateAPIView):
#     queryset = Measurement.objects.all()
#     serializer_class = MeasurementSerializer

    # def post(self, request):
    #     try:
    #         sensor = request.data.get('sensor_id')
    #         sensor = Sensor.objects.get(id=sensor)
    #         temperature = request.data.get('temperature')
    #         image_optional = request.data.get('image_optional', None)
    #         Measurement(
    #             sensor=sensor,
    #             temperature=temperature,
    #             image_optional=image_optional
    #             ).save()
    #         return Response({'status': 'ok'})
    #     except Exception as e:
    #         return Response({'status': 'error', 'exception': f'{e}'})


# добавление измерения
class MeasurementView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


