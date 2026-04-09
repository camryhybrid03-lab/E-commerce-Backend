from django.db import transaction
from django.db.models import F
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import CartItemReadSerializer, CartItemWriteSerializer, CartSerializer
from catalog.models import Product
from orders.services import checkout_cart_to_order
class CartDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = (
            Cart.objects.select_related("user")
            .prefetch_related("items__product")
            .filter(user=request.user)
            .first()
        )
        if not cart:
            cart = Cart.objects.create(user=request.user)
        return Response(CartSerializer(cart).data)


class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return (
            CartItem.objects.select_related("cart", "product")
            .filter(cart__user=self.request.user)
            .order_by("-id")
        )

    def get_serializer_class(self):
        if self.action in {"create", "partial_update", "update"}:
            return CartItemWriteSerializer
        return CartItemReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product: Product = serializer.validated_data["product"]
        qty: int = serializer.validated_data["quantity"]

        cart, _ = Cart.objects.get_or_create(user=request.user)

        with transaction.atomic():
            item, created = CartItem.objects.select_for_update().get_or_create(
                cart=cart, product=product, defaults={"quantity": qty}
            )
            if not created:
                item.quantity = F("quantity") + qty
                item.save(update_fields=["quantity", "updated_at"])
                item.refresh_from_db()

        return Response(
            CartItemReadSerializer(item).data, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request):
        order = checkout_cart_to_order(user=request.user)
        return Response({"order_id": order.id}, status=status.HTTP_201_CREATED)
