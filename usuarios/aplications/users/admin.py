""" Admin de la aplicacion users """

from django.contrib import admin

from .models import User
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Configuracion del admin para el modelo User """

    list_display = ('username', 'email', 'nombres', 'apellidos', 'genero', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'nombres', 'apellidos')
    list_filter = ('genero', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('username',)
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Informacion Personal', {
            'fields': ('nombres', 'apellidos', 'genero')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )