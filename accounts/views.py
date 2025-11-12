from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .models import Usuario
import json, requests

@csrf_exempt
def usuarios(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        nombre = (data.get("nombre") or "").strip()
        email  = (data.get("email") or "").strip()
        tel    = (data.get("tel") or "").strip()

        user = Usuario.objects.create(nombre=nombre, email=email, tel=tel)

        notify_url = getattr(settings, "NOTIFY_URL", "http://127.0.0.1:8001/notify")
        notify_key = getattr(settings, "NOTIFY_KEY", "super-secreta")
        payload = {
            "event": "user_created",
            "to": [email],
            "subject": "Registro OK",
            "html": f"<b>Bienvenido, {nombre}!</b>",
            "text": f"Bienvenido, {nombre}!",
        }
        try:
            requests.post(
                notify_url,
                json=payload,
                headers={"X-API-Key": notify_key, "Content-Type": "application/json"},
                timeout=5,
            )
        except Exception:
            pass 

        return JsonResponse(
            {"ok": True, "id": user.id, "nombre": nombre, "email": email, "tel": tel},
            status=201,
        )

    if request.method == "GET":
        usuarios = list(Usuario.objects.values("id", "nombre", "email", "tel"))
        return JsonResponse(usuarios, safe=False)

    return JsonResponse({"error": "Método no permitido"}, status=405)
