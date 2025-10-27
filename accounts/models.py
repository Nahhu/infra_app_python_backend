from django.core.validators import validate_email
from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, validators=[validate_email])
    tel = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.nombre} ({self.email})"