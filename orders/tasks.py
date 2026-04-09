from celery import shared_task

from orders.models import Order


@shared_task
def send_order_created_email(order_id: int) -> None:
    order = (
        Order.objects.select_related("user")
        .prefetch_related("items__product")
        .get(id=order_id)
    )

    lines = [
        f"To: {order.user.email or '(no-email)'}",
        f"Subject: Order #{order.id} created",
        "",
        f"Hello {order.user.username},",
        f"Your order #{order.id} has been created successfully.",
        "",
        "Items:",
    ]
    for item in order.items.all():
        lines.append(
            f"- {item.product.sku} | {item.product.name} | qty={item.quantity} | unit_price={item.unit_price}"
        )
    lines.append("")
    lines.append(f"Total: {order.total_amount}")
    lines.append("")
    print("\n".join(lines))

