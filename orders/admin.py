from django.contrib import admin

# Register your models here.
from .models import menuCategory, regularPizza, sicilianPizza, pizzaToppings, dinnerPlatter, salad, pasta, subs, cart, orderList, addOn

admin.site.register(orderList)
admin.site.register(cart)
admin.site.register(menuCategory)
admin.site.register(regularPizza)
admin.site.register(sicilianPizza)
admin.site.register(pizzaToppings)
admin.site.register(dinnerPlatter)
admin.site.register(salad)
admin.site.register(pasta)
admin.site.register(subs)
admin.site.register(addOn)
