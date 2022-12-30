from django.db import models


class TimestampFields(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class Sensor(TimestampFields):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ['created_at']


class Measurement(TimestampFields):
    temperature = models.FloatField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    image_optional = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ['created_at']


