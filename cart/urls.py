from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cart.views import CartDetailView, CartItemViewSet

router = DefaultRouter()
router.register("cart/items", CartItemViewSet, basename="cart-item")

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart-detail"),
    path("", include(router.urls)),
]

