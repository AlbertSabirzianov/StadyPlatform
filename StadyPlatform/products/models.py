from django.contrib.auth import get_user_model
from django.db import models

from StadyPlatform.settings import PERCENT_OF_PASSED_LESSON
from .validators import url_path_validator
from api.utils import get_percentage

User = get_user_model()


class Lesson(models.Model):
    """
    Урок,может находится в разных продуктах.
    """

    name = models.CharField(max_length=200)
    link = models.CharField(
        max_length=500,
        validators=[url_path_validator],
        verbose_name='Ссылка на видио урок'
    )
    length = models.IntegerField(
        verbose_name='Длинна видио в минутах'
    )


class Product(models.Model):
    """
    Продукт, у которого есть владелец owner.
    """

    owner = models.ForeignKey(
        User,
        related_name='products',
        on_delete=models.PROTECT,
        verbose_name='Владелец'
    )
    lessons = models.ManyToManyField(
        Lesson,
        related_name='products',
        verbose_name='Уроки'
    )


class Availability(models.Model):
    """
    Доступ юзера к продукту.
    """

    user = models.ForeignKey(
        User,
        related_name='availability',
        on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Product,
        related_name='availability',
        on_delete=models.PROTECT
    )
    is_available = models.BooleanField(
        verbose_name='Доступен ли продукт'
    )


class Result(models.Model):
    """
    Фиксатор времени и статуса просмотра урока.
    """

    user = models.ForeignKey(
        User,
        related_name='results',
        on_delete=models.PROTECT
    )
    lesson = models.ForeignKey(
        Lesson,
        related_name='results',
        on_delete=models.PROTECT
    )
    viewed_time = models.IntegerField(
        default=0
    )

    def is_passed(self) -> bool:
        """
        Просмотренн ли ролик.
        """

        viewed_percent = get_percentage(self.viewed_time, self.lesson.length)
        return viewed_percent >= PERCENT_OF_PASSED_LESSON
