from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import serializers

from advertisements.models import Advertisement

from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        # TODO: добавьте требуемую валидацию
        request = self.context["request"]
        ads_quantity = Advertisement.objects.filter(creator=request.user, status='OPEN').\
            values('status').annotate(the_count=Count("status"))

        if request.method in ['POST', 'PATCH', 'PUT']:
            for each in ads_quantity:
                if each['the_count'] >= 10:
                    raise ValidationError('Ошибка публикации: у Вас 10 или более открытых объявлений')
        return data
