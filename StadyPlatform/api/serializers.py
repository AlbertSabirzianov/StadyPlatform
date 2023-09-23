from django.contrib.auth import get_user_model
from rest_framework import serializers

from products.models import Result, Lesson, Product, Availability
from .utils import get_percentage

User = get_user_model()


class ResultSerializer(serializers.ModelSerializer):
    """Сериализация времени и статуса просмотра урока."""

    class Meta:
        model = Result
        fields = (
            'viewed_time',
            'is_passed'
        )


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация уроков."""

    status = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'name',
            'link',
            'length',
            'status'
        )

    def get_status(self, obj):
        """Достаём Результаты занятий пользователя по урокам."""

        result = Result.objects.get_or_create(
            user=self.context['request'].user,
            lesson=obj
        )[0]
        return ResultSerializer(instance=result).data


class ProductStatisticSerializer(serializers.ModelSerializer):
    """Сериализация статистики по продуктам."""

    sum_of_passed_lessons = serializers.SerializerMethodField()
    sum_of_viewed_time = serializers.SerializerMethodField()
    count_students = serializers.SerializerMethodField()
    shopping_percent = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'sum_of_passed_lessons',
            'sum_of_viewed_time',
            'count_students',
            'shopping_percent'
        )

    @staticmethod
    def get_results_of_product(obj):
        """
        Получаем Результаты прохождения урока только учеников, купивших продукт.
        """

        return Result.objects.filter(
            lesson__in=obj.lessons.all(),
            user__availability__is_available=True,
            user__availability__product=obj
        )

    def get_sum_of_passed_lessons(self, obj) -> int:
        """
        Колличество просмотренных уроков от всех учеников.
        """

        count = 0
        for result in self.get_results_of_product(obj):
            if result.is_passed():
                count += 1
        return count

    def get_sum_of_viewed_time(self, obj) -> int:
        """
        Сколько в сумме все ученики потратили времени на
        просмотр роликов.
        """

        results = self.get_results_of_product(obj)
        return sum([result.viewed_time for result in results])

    def get_count_students(self, obj) -> int:
        """
        Колличество учеников, занимающихся на продукте.
        """

        return User.objects.filter(
            availability__is_available=True,
            availability__product=obj
        ).count()

    def get_shopping_percent(self, obj) -> float:
        """
        Процент приобретения продукта.
        """

        all_users_count = User.objects.filter(is_staff=False).count()
        availability_count = Availability.objects.filter(
            is_available=True,
            product=obj
        ).count()
        return get_percentage(availability_count, all_users_count)
