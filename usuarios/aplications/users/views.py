"""" Views de la aplicacion users """

from django.core.mail import send_mail # Importar la función para enviar correos
from django.views.generic.edit import FormView # Importar la vista genérica edicion FormView
from django.views.generic import ListView # Importar la vista genérica ListView
from django.views import View # Importar la vista genérica View
from django.contrib.auth.mixins import LoginRequiredMixin # Importar el mixin para requerir login
# Importar las funciones de autenticación
from django.contrib.auth import (login, logout) # Importar las funciones para login y logout
from django.contrib.auth.forms import AuthenticationForm # Importar el formulario de autenticación
from django.shortcuts import redirect # Importar la función para redirigir
from django.urls import reverse_lazy # Importar reverse_lazy para redirecciones perezosas
from usuarios.settings.base import get_secret # Importar la función get_secret para obtener secretos
from .models import User # Importar el modelo User
# Importar los formularios
from .forms import (UserRegisterForm,
                    # UserLoginForm,
                    UpdatePasswordForm,
                    CodigoVerificacionForm)
from .processor import code_generator # Importar la función para generar códigos aleatorios

# Create your views here.


class UserRegisterView(FormView):
    """ Vista para el registro de usuarios """
    template_name = 'users/register.html' # Template para el registro de usuarios
    success_url = reverse_lazy('users:verificar-codigo') # Redirigir a la verificacion de codigo despues del registro
    queryset = User.objects.all() # Queryset de usuarios todos los usuarios
    form_class = UserRegisterForm # Formulario para el registro de usuarios


    def form_valid(self, form):
        """ Si el formulario es valido, guardar el usuario """
        user = form.save(commit=False) # Crear el usuario sin guardar
        user.set_password(form.cleaned_data['password']) # Establecer la contraseña hasheada
        user.is_active = False # Desactivar el usuario hasta que verifique su correo
        codigo = code_generator() # Generar un codigo verificador
        user.codigo_verificador = codigo # Asignar el codigo verificador al usuario
        user.save() # Guardar el usuario
        # Enviar correo con el codigo verificador
        send_mail(
            'Codigo Verificador', # Asunto del correo
            f'Tu codigo verificador es: {codigo}', # Mensaje del correo
            get_secret('EMAIL_HOST_USER'), # Correo remitente
            [user.email], # Correo destinatario
            fail_silently=False, # No fallar silenciosamente
        )
        # Redirigir a la verificacion de codigo
        return super(UserRegisterView, self).form_valid(form)


class VerificarCodigoView(FormView):
    """ Vista para verificar el codigo de verificacion """

    template_name = 'users/verificar_codigo.html' # Template para verificar el codigo
    success_url = reverse_lazy('users:login') # Redirigir al login si el codigo es correcto
    form_class = CodigoVerificacionForm # Formulario para verificar el codigo


    def form_valid(self, form):
        """ Si el formulario es valido, verificar el codigo """
        # Recuperamos el usuario validado desde el formulario
        username = form.cleaned_data['username'] # Obtener el nombre de usuario ejemplo: Usuario123
        usuario = User.objects.get(username=username) # Obtener el usuario por su nombre de usuario

        # Activamos el usuario
        usuario.is_active = True
        usuario.save() # Guardar los cambios en el usuario
        # Redirigir al login
        return super(VerificarCodigoView, self).form_valid(form)


class LoginView(FormView):
    """ Vista para el login de usuarios """

    template_name = 'users/login.html' # Template para el login
    form_class = AuthenticationForm # Formulario de autenticacion
    success_url = reverse_lazy('home:home') # Redirigir a la pagina principal despues del login

    def form_valid(self, form):
        """ Si el formulario es valido, autenticar y loguear al usuario """

        user = form.get_user()  # El usuario ya viene autenticado
        login(self.request, user) # Loguear al usuario
        return super().form_valid(form) # Redirigir a la pagina principal


class UserLogoutView(View):
    """ Vista para el logout de usuarios """

    def get(self, request):
        """ Cerrar sesion del usuario """
        logout(request) # Cerrar sesion del usuario
        return redirect('home:home') # Redirigir a la pagina principal


class UserLista(LoginRequiredMixin, ListView):
    """ Vista para listar los usuarios """

    login_url = reverse_lazy('users:login') # Redirigir al login si no esta autenticado
    model = User # Modelo de usuario
    queryset = User.objects.listar_usuarios() # Queryset de usuarios
    template_name = 'users/user_list.html' # Template para listar los usuarios
    context_object_name = 'users' # Nombre del contexto para los usuarios
    paginate_by = 10 # Paginacion de 10 usuarios por pagina
    ordering = ['username'] # Ordenar por nombre de usuario
    template_name_suffix = '_list' # Sufijo del template
    allow_empty = True # Permitir lista vacia
    page_kwarg = 'page' # Nombre del parametro de pagina
    paginate_orphans = 0 # Numero de objetos huérfanos permitidos en la última página
    extra_context = {'title': 'Lista de Usuarios'} # Contexto extra para el template


    def get_queryset(self):
        """ Retorna el queryset de usuarios """
        return self.queryset # Retornar el queryset de usuarios


class UpdatePasswordView(LoginRequiredMixin, FormView):
    """ Vista para actualizar la contraseña del usuario """

    login_url = reverse_lazy('users:login') # Redirigir al login si no esta autenticado
    template_name = 'users/update_password.html' # Template para actualizar la contraseña
    success_url = '/' # Redirigir a la pagina principal despues de actualizar la contraseña
    form_class = UpdatePasswordForm # Formulario para actualizar la contraseña

    def get_form_kwargs(self):
        """ Pasar el usuario actual al formulario """
        kwargs = super().get_form_kwargs() # Obtener los argumentos del formulario
        kwargs['user'] = self.request.user # Pasar el usuario actual
        return kwargs # Retornar los argumentos del formulario

    def form_valid(self, form):
        """ Si el formulario es válido, actualizar la contraseña """
        user = self.request.user # Obtener el usuario actual
        nueva_password = form.cleaned_data['password_nueva'] # Obtener la nueva contraseña

        user.set_password(nueva_password) # Establecer la nueva contraseña
        user.save() # Guardar el usuario

        # Mantener al usuario logueado después del cambio
        from django.contrib.auth import update_session_auth_hash # Importar la función para actualizar la sesión
        update_session_auth_hash(self.request, user) # Actualizar la sesión del usuario

        return super().form_valid(form) # Redirigir a la pagina principal

