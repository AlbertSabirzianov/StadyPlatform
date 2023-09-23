from django.urls import path, include

from rest_framework.routers import SimpleRouter


from .views import LessonViewSet, ProductViewSet

app_name = 'api'

router = SimpleRouter()
router.register('lessons', LessonViewSet, basename='lesson')
router.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls))
]
