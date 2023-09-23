from django.contrib import admin

from .models import Product, Lesson, Result, Availability


admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Result)
admin.site.register(Availability)
