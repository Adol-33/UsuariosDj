""" Endpoints de la aplicacion home """

from django.urls import path
from .views import HomePageView

app_name = 'home'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]

