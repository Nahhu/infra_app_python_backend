from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import UsuarioSerializer
import requests  # Para comunicarte con el servicio de correo

API_CORREO_URL = "http://localhost:5000/api/enviar_correo"

@api_view(['GET', 'POST'])
def usuarios(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()

            # Enviar correo (si el servicio está activo)
            try:
                requests.post(API_CORREO_URL, json={
                    "email": usuario.email,
                    "nombre": usuario.nombre
                })
            except Exception as e:
                print("⚠️ Error enviando correo:", e)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
