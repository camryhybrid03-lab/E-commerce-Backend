from rest_framework import permissions, viewsets

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects.select_related("user")
            .prefetch_related("items__product")
            .filter(user=self.request.user)
            .order_by("-id")
        )
