# accounts/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json, requests

@csrf_exempt
def usuarios(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        nombre = (data.get("nombre") or "").strip()
        email  = (data.get("email") or "").strip()
        tel    = (data.get("tel") or "").strip()

        # TODO: acá guardás en tu modelo real (ej: Usuario(nombre=..., email=..., tel=...).save())

        # 🔔 disparar mail al microservicio
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
            r = requests.post(
                notify_url,
                json=payload,
                headers={"X-API-Key": notify_key, "Content-Type": "application/json"},
                timeout=5,
            )
            # debug opcional:
            # print("NOTIFY ->", r.status_code, r.text)
        except Exception:
            pass  # en prod: log.exception(...)

        return JsonResponse({"ok": True, "nombre": nombre, "email": email, "tel": tel}, status=201)

    if request.method == "GET":
        # TODO: devolvé tu lista real desde la BD
        return JsonResponse([], safe=False)

    return JsonResponse({"error": "Método no permitido"}, status=405)
