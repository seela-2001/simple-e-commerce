from django.contrib import admin
from .models import Product,Order,Review,OrderItem,Order_Products
# Register your models here.
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Order_Products)