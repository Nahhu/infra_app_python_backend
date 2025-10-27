# accounts/urls.py
from django.urls import path
from .views import usuarios

urlpatterns = [
    path("api/usuarios/", usuarios, name="usuarios"),
]
