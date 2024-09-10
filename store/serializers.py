from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product,Review,Order,ShippingAddress,OrderItem,Order_Products

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    # order_item = serializers.SerializerMethodField(read_only = True)
    # def get_order_item(self,obj):
    #     return obj.product.id
    class Meta:
        model = OrderItem
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only = True)

    def get_product(self,obj):
        return obj.product.name

    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only = True)
    def get_reviews(self,obj):
        reviews = Review.objects.filter(product=obj)
        serializer = ReviewSerializer(reviews,many=True)
        return serializer.data
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    shipping_address = ShippingAddressSerializer(source='order_shipping', read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = '__all__'



class OrderProductSerializer(serializers.ModelSerializer):
    model = Order_Products
    fields = '__all__'


