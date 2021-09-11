from django.db import models
import re
from datetime import date

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

class ViajesManager(models.Manager):
    def validador_basico(self, postData):

        errors = {}

        fecha_actual = date.today().strftime('%Y-%m-%d')

        if len(postData['destino']) < 1:
            errors['destino'] = "El Destino es un campo requerido"

        if len(postData['plan']) < 1:
            errors['plan'] = "El Plan es un campo requerido"

        if postData['fecha_partida'] < fecha_actual:    
            errors["fecha_partida"] ="La Fecha de Partida debe ser igual o superior a la fecha actual"
            
        if postData['fecha_partida'] > postData['fecha_salida']:    
            errors["fecha_partida"] ="La Fecha de Llegada no puede ser inferior a la fecha de partida"
        
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
    fecha_partida = models.DateField()
    fecha_salida = models.DateField()
    plan = models.CharField(max_length=255)
    travellers = models.ManyToManyField(User, related_name="viajeros")
    creater = models.ForeignKey(User,related_name = "creador", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ViajesManager()

    def __str__(self):
        return f"{self.destino}: {self.travellers}:{self.creater}"

    def __repr__(self):
        return f"{self.destino}: {self.travellers}:{self.creater}"

