

from django.db import models

from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager, models.Manager):
    """ Manager para el modelo de usuario personalizado """

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """ Crea y retorna un usuario normal """
        user = self.model(username=username, email=email, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,  username, email, password=None, **extra_fields):
        """ Crea y retorna un usuario normal """
        return self._create_user(
            username=username,
            email=email,
            password=password,
            is_staff=False,
            is_superuser=False,
            **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        """ Crea y retorna un superusuario """
        return self._create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields)

