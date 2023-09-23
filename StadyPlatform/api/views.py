from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.serializers import LessonSerializer, ProductStatisticSerializer
from products.models import Lesson, Product
from .utils import SAFE_ACTIONS

"""
1 - '/api/lessons/'
2 - '/api/products/<id>/lessons/'
3 - '/api/products/'
"""


class LessonViewSet(ReadOnlyModelViewSet):
    """Представление доступных пользователю уроков."""

    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        """Выбираем уроки, которые доступны пользователю."""

        queryset = Lesson.objects.filter(
            products__availability__user=self.request.user,
            products__availability__is_available=True
        )
        return queryset


class ProductViewSet(ReadOnlyModelViewSet):
    """Передставление доступных пользователю продуктов."""

    permission_classes = [IsAuthenticated]
    serializer_class = ProductStatisticSerializer

    def get_queryset(self):
        """
        Выбираем все продукты, если нужна статистика,
        Выбираем продукты, которые доступны пользователю,
        если нужно получить информацию по урокам.
        """

        if self.action in SAFE_ACTIONS:
            return Product.objects.all()

        queryset = Product.objects.filter(
            availability__user=self.request.user,
            availability__is_available=True
        )
        return queryset

    @action(detail=True)
    def lessons(self, *args, **kwargs):
        product = self.get_object()
        serializer = LessonSerializer(
            instance=product.lessons,
            many=True,
            context={'request': self.request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
