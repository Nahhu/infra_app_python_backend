from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import requests

User = get_user_model()

NOTIFY_URL = getattr(settings, "NOTIFY_URL", "http://127.0.0.1:8001/notify")
NOTIFY_KEY = getattr(settings, "NOTIFY_KEY", "super-secreta")

@receiver(post_save, sender=User)
def on_user_created(sender, instance, created, **kwargs):
    if not created or not getattr(instance, "email", None):
        return

    payload = {
        "event": "user_created",
        "to": [instance.email],
        "subject": "Registro OK",
        "html": f"<b>Bienvenido, {instance.get_full_name() or instance.username}!</b>",
        "text": f"Bienvenido, {instance.get_full_name() or instance.username}!",
    }

    try:
        resp = requests.post(
            NOTIFY_URL,
            json=payload,
            headers={"X-API-Key": NOTIFY_KEY, "Content-Type": "application/json"},
            timeout=5,
        )
        print("NOTIFY ->", resp.status_code, resp.text)  
    except Exception as e:
        print("NOTIFY ERROR:", repr(e))
