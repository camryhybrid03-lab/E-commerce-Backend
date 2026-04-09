from rest_framework import serializers

from cart.models import Cart, CartItem
from catalog.models import Product
from catalog.serializers import ProductSerializer


class CartItemWriteSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]
        read_only_fields = ["id"]

    def validate_quantity(self, value: int) -> int:
        if value <= 0:
            raise serializers.ValidationError("quantity must be > 0")
        return value


class CartItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "created_at", "updated_at"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "created_at", "updated_at"]

