from django.contrib import admin
from .models import food , Review , user_details , orders
# Register your models here.

admin.site.register(food)
admin.site.register(Review)
admin.site.register(orders)
admin.site.register(user_details)