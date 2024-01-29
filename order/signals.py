import redis
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

# Redis 클라이언트 설정
redis_client = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)


@receiver(post_save, sender=Order)
def send_sse_event(sender, instance, created, **kwargs):
    if created:
        message = f"New order created: {instance.name}"
        redis_client.publish("new_orders", message)
