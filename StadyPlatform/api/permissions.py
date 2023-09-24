from rest_framework.permissions import BasePermission

from products.models import Availability


class IsAvailableProduct(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Есть ли у юзера доступ к продукту
        """

        return Availability.objects.filter(
            product=obj,
            user=request.user,
            is_available=True
        ).exists()
