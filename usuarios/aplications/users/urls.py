""" ENdpoint de urls para la aplicacion de usuarios """

from django.urls import path
from .views import UserRegisterView, LoginView, UserLogoutView, UserLista, UpdatePasswordView, VerificarCodigoView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('lista/', UserLista.as_view(), name='user-list'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password'),
    path('verificar-codigo/', VerificarCodigoView.as_view(), name='verificar-codigo'),
]
