import random

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from products.models import Lesson, Availability, Product

from art import text2art

User = get_user_model()


def push_users():
    print('push users.....')
    User.objects.create_user(username='al', password='123'),
    User.objects.create_user(username='ken', password='321'),
    User.objects.create_user(username='owner', password='543321')


def push_lessons():
    print('push lessons...')
    Lesson.objects.bulk_create(
        [Lesson(
            name='lesson_' + str(num),
            length=random.randint(20, 50),
            link='https://youtube.ru'
        ) for num in range(50)]
    )


def push_products():
    print('push products...')
    product_1 = Product.objects.create(
        owner=User.objects.get(username='owner')
    )
    for num in range(20):
        product_1.lessons.add(
            Lesson.objects.get(name='lesson_' + str(num))
        )

    product_2 = Product.objects.create(
        owner=User.objects.get(username='owner')
    )
    for num in range(21, 30):
        product_2.lessons.add(
            Lesson.objects.get(name='lesson_' + str(num))
        )


def push_availability():
    print('push availability....')
    Availability.objects.create(
        user=User.objects.get(username='al'),
        product=Product.objects.first(),
        is_available=True
    )
    Availability.objects.create(
        user=User.objects.get(username='ken'),
        product=Product.objects.last(),
        is_available=True
    )


class Command(BaseCommand):
    """
    Добавляем тестовые данные в базу.
    """

    def handle(self, *args, **options):
        print(text2art('start'))
        push_users()
        push_lessons()
        push_products()
        push_availability()
        print(text2art('success'))
