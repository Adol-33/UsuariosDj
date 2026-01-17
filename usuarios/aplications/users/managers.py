

from django.db import models

from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager, models.Manager):
    """ Manager para el modelo de usuario personalizado """

    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):
        """ Crea y retorna un usuario normal """

        # Recibir todos los parametros necesarios para crear un usuario
        user = self.model(username=username, # Asignar el nombre de usuario
                          email=email, # Asignar el correo electrónico
                          is_staff=is_staff, # Asignar si es staff
                          is_superuser=is_superuser, # Asignar si es superusuario
                          is_active=is_active, # Asignar si está activo
                          **extra_fields) # Asignar campos extra

        user.set_password(password) # Establecer la contraseña hasheada
        user.save(using=self._db) # Guardar el usuario en la base de datos
        return user # Retornar el usuario creado

    def create_user(self,  username, email, password=None, **extra_fields):
        """ Crea y retorna un usuario normal """
        return self._create_user(
            username=username, # Asignar el nombre de usuario
            email=email, # Asignar el correo electrónico
            password=password, # Asignar la contraseña
            is_staff=False, # No es staff
            is_superuser=False, # No es superusuario
            is_active=True, # Está activo
            **extra_fields) # Asignar campos extra

    def create_superuser(self, username, email, password=None, **extra_fields):
        """ Crea y retorna un superusuario """

        return self._create_user(
            username=username, # Asignar el nombre de usuario
            email=email, # Asignar el correo electrónico
            password=password, # Asignar la contraseña
            is_staff=True, # Es staff
            is_superuser=True, # Es superusuario
            is_active=True, # Está activo
            **extra_fields) # Asignar campos extra

    def listar_usuarios(self):
        """ Retorna una lista de todos los usuarios """
        return self.all() # Retornar todos los usuarios

    def buscar_por_email(self, email):
        """ Retorna un usuario por su correo electrónico """
        return self.get(email=email) # Retornar el usuario con el correo electrónico dado

    def buscar_por_username(self, username):
        """ Retorna un usuario por su nombre de usuario """
        return self.get(username=username) # Retornar el usuario con el nombre de usuario dado

    def eliminar_usuario(self, username):
        """ Elimina un usuario por su nombre de usuario """
        usuario = self.get(username=username) # Obtener el usuario por su nombre de usuario
        usuario.is_active = False # Desactivar el usuario
        usuario.save() # Guardar los cambios en el usuario
        return usuario # Retornar el usuario eliminado

    def activar_usuario(self, username):
        """ Activa un usuario por su nombre de usuario """
        usuario = self.get(username=username) # Obtener el usuario por su nombre de usuario
        usuario.is_active = True # Activar el usuario
        usuario.save() # Guardar los cambios en el usuario
        return usuario # Retornar el usuario activado

    def actualizar_contraseña(self, username, new_password):
        """ Actualiza la contraseña de un usuario por su nombre de usuario """
        usuario = self.get(username=username) # Obtener el usuario por su nombre de usuario
        usuario.set_password(new_password) # Establecer la nueva contraseña hasheada
        usuario.save() # Guardar los cambios en el usuario
        return usuario # Retornar el usuario con la contraseña actualizada

    def actualizar_email(self, username, new_email):
        """ Actualiza el correo electrónico de un usuario por su nombre de usuario """
        usuario = self.get(username=username) # Obtener el usuario por su nombre de usuario
        usuario.email = new_email # Establecer el nuevo correo electrónico
        usuario.save() # Guardar los cambios en el usuario
        return usuario # Retornar el usuario con el correo electrónico actualizado

    def actualizar_nombre_completo(self, username, new_full_name):
        """ Actualiza el nombre completo de un usuario por su nombre de usuario """
        usuario = self.get(username=username) # Obtener el usuario por su nombre de usuario
        usuario.full_name = new_full_name # Establecer el nuevo nombre completo
        usuario.save() # Guardar los cambios en el usuario
        return usuario # Retornar el usuario con el nombre completo actualizado

    def usuarios_activos(self):
        """ Retorna una lista de usuarios activos """
        return self.filter(is_active=True) # Retornar los usuarios que están activos

    def usuarios_inactivos(self):
        """ Retorna una lista de usuarios inactivos """
        return self.filter(is_active=False) # Retornar los usuarios que están inactivos

    def contar_usuarios(self):
        """ Retorna el número total de usuarios """
        return self.count() # Retornar el conteo de usuarios

    def contar_usuarios_activos(self):
        """ Retorna el número de usuarios activos """
        return self.filter(is_active=True).count() # Retornar el conteo de usuarios activos

    def contar_usuarios_inactivos(self):
        """ Retorna el número de usuarios inactivos """
        return self.filter(is_active=False).count() # Retornar el conteo de usuarios inactivos

    def buscar_por_codigo_verificador(self, codigo):
        """ Retorna un usuario por su código verificador """
        return self.get(codigo_verificador=codigo) # Retornar el usuario con el código verificador dado



