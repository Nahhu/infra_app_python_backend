from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    tel = models.CharField(max_length=9)

    def __str__(self):
        return self.nombre