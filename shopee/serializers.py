from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    # imageURL = serializers.ReadOnlyField()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        lookup_field = 'slug'

class ShopProductSerializer(serializers.ModelSerializer):
    imageURL = serializers.ReadOnlyField()
    class Meta:
        model = Product
        fields = "__all__"
        lookup_field = 'category'


class OrderSerializer(serializers.ModelSerializer):
    shipping = serializers.ReadOnlyField()
    get_cart_total = serializers.ReadOnlyField()
    get_cart_items = serializers.ReadOnlyField()
    class Meta:
        model = Order
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    get_total = serializers.ReadOnlyField()
    get_item_name = serializers.ReadOnlyField()
    get_item_img = serializers.ReadOnlyField()
    get_item_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = "__all__"

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = "__all__"


class RecomSerializer(serializers.ModelSerializer):
    recoImageURL = serializers.ReadOnlyField()

    class Meta:
        model = Recom
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    get_person_name = serializers.ReadOnlyField()
    class Meta:
        model = Comment
        fields = "__all__"