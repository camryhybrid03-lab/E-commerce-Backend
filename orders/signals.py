from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from orders.tasks import send_order_created_email


@receiver(post_save, sender=Order)
def order_created_send_email(sender, instance: Order, created: bool, **kwargs):
    if not created:
        return

    transaction.on_commit(lambda: send_order_created_email.delay(instance.id))

