""" Modelos de la aplicacion de usuarios """

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import UserManager
# Create your models here.

class User(AbstractUser, PermissionsMixin):
    """ Modelo de usuario personalizado """
    genero_choice = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )
    username = models.CharField('User Name', max_length=10, unique=True)
    email = models.EmailField('Email Address', unique=True)
    nombres = models.CharField('First Names', max_length=100, blank=True)
    apellidos = models.CharField('Last Names', max_length=100, blank=True)
    genero = models.CharField('Genero', max_length=1, choices=(genero_choice), blank=True)
    codigo_verificador = models.CharField('Codigo Verificador', max_length=6, blank=True)
    is_active = models.BooleanField('Activo', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_short_name(self)-> str:
        """ Retorna el nombre corto del usuario """
        return self.username

    def get_full_name(self)-> str:
        """ Retorna el nombre completo del usuario """
        return f"{self.nombres} {self.apellidos}"

