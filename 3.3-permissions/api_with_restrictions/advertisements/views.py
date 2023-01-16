from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorites, AdvertisementStatusChoices
from advertisements.permissions import IsOwnerOrReadonlyOrIsAdmin
from advertisements.serializers import AdvertisementSerializer, AdvertisementFavSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadonlyOrIsAdmin, IsAdminUser, IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy", ]:
            return [IsAuthenticated(), IsOwnerOrReadonlyOrIsAdmin()]  # or [IsAdminUser()]
        return []

    def get_queryset(self):
        queryset = Advertisement.objects.exclude(status='DRAFT')
        if self.request.user.is_authenticated:
            user_drafts = Advertisement.objects.filter(creator=self.request.user,
                                                       status=AdvertisementStatusChoices.DRAFT)
            queryset = queryset | user_drafts
        return queryset


class AdvertisementFavViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementFavSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    # просмотр избранного
    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def favorites(self, request):
        user = request.user
        favorite_ids = user.favorites.values_list('advertisement', flat=True)
        ads = Advertisement.objects.filter(id__in=favorite_ids)
        serializer = AdvertisementSerializer(ads, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def add_to_favorites(self, request):
        adv_id = request.data.get("id")

        try:
            advertisement = Advertisement.objects.get(id=adv_id)
        except Exception as err:
            return Response(f'Ошибка добавления в избранное: {err}', status=status.HTTP_400_BAD_REQUEST)
        if advertisement.creator == request.user:
            return Response('Нельзя добавлять в избранное своё объявление', status=status.HTTP_400_BAD_REQUEST)
        elif Favorites.objects.filter(advertisement=advertisement, user=request.user).exists():
            return Response('Объявление уже добавлено в избранное', status=status.HTTP_400_BAD_REQUEST)
        else:
            Favorites.objects.create(advertisement=advertisement, user=request.user)
            return Response('Объявление добавлено в избранное', status=status.HTTP_200_OK)
