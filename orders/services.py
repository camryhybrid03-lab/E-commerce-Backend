from decimal import Decimal

from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError

from cart.models import Cart, CartItem
from catalog.models import Product
from orders.models import Order, OrderItem


def checkout_cart_to_order(*, user) -> Order:
    cart = (
        Cart.objects.select_related("user")
        .prefetch_related("items__product")
        .filter(user=user)
        .first()
    )
    if not cart:
        raise ValidationError({"cart": "cart is empty"})

    items = list(cart.items.all())
    if not items:
        raise ValidationError({"cart": "cart is empty"})

    with transaction.atomic():
        # Lock products rows to avoid oversell.
        product_ids = [i.product_id for i in items]
        products = {
            p.id: p
            for p in Product.objects.select_for_update().filter(id__in=product_ids)
        }

        for item in items:
            p = products[item.product_id]
            if item.quantity > p.stock_qty:
                raise ValidationError(
                    {"stock": f"Insufficient stock for sku={p.sku} (have={p.stock_qty})"}
                )

        order = Order.objects.create(user=user, status=Order.Status.CREATED)

        total = Decimal("0")
        order_items = []
        for item in items:
            p = products[item.product_id]
            unit_price = p.price
            total += unit_price * item.quantity
            order_items.append(
                OrderItem(
                    order=order,
                    product=p,
                    quantity=item.quantity,
                    unit_price=unit_price,
                )
            )

            Product.objects.filter(id=p.id).update(stock_qty=F("stock_qty") - item.quantity)

        OrderItem.objects.bulk_create(order_items)
        Order.objects.filter(id=order.id).update(total_amount=total)
        order.refresh_from_db()

        CartItem.objects.filter(cart=cart).delete()

    return order

