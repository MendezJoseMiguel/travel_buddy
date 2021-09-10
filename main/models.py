from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['name']) < 2:
            errors['name'] = "nombre debe tener al menos 2 caracteres de largo"

        if len(postData['username']) < 2:
            errors['username'] = "nombre debe tener al menos 2 caracteres de largo"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

        if not SOLO_LETRAS.match(postData['name']):
            errors['solo_letras'] = "solo letras en nombre por favor"

        if len(postData['password']) < 8:
            errors['password'] = "contraseña debe tener al menos 8 caracteres"

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        
        return errors


class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.name}: {self.username}"

    def __repr__(self):
        return f"{self.name}: {self.username}"

class Viajes(models.Model):
    destino = models.CharField(max_length=255)
    fecha_partida = models.DateTimeField()
    fecha_salida = models.DateTimeField()
    plan = models.CharField(max_length=255)
    viajeros = models.ManyToManyField(User, related_name="viajeros")
    creador = models.ForeignKey(User,related_name = "creador", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.destino}: {self.viajeros}:{self.creador}"

    def __repr__(self):
        return f"{self.destino}: {self.viajeros}:{self.creador}"

