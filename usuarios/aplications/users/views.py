"""" Views de la aplicacion users """

#from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import User
from .forms import UserRegisterForm, UserLoginForm

# Create your views here.


class UserRegisterView(FormView):
    """ Vista para el registro de usuarios """

    template_name = 'users/register.html'
    success_url = '/'
    queryset = User.objects.all()
    form_class = UserRegisterForm

    def form_valid(self, form):
        """ Si el formulario es valido, guardar el usuario """
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super(UserRegisterView, self).form_valid(form)


class LoginView(FormView):
    """ Vista para el login de usuarios """

    template_name = 'users/login.html'
    success_url = '/'
    form_class = UserLoginForm
    
    def form_valid(self, form):
        """ Si el formulario es valido, autenticar el usuario """
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginView, self).form_valid(form)


class UserLogoutView(View):
    """ Vista para el logout de usuarios """
    
    def get(self, request):
        """ Cerrar sesion del usuario """
        logout(request)
        return redirect('home:home')

