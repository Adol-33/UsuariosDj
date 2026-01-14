"""" Configuraciones de las URLs del proyecto usuarios """


from django.contrib import admin
from django.urls import path, include
from aplications.users import urls
from aplications.home import urls as home_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(urls, namespace='users')),
    path('', include(home_urls, namespace='home')),
]
