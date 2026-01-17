""" Formularios para la aplicacion de usuarios """

from django import forms
from .models import User


class UserRegisterForm(forms.ModelForm):
    """ Formulario para el registro de usuarios """
    # Campo adicional para confirmar la contraseña
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Confirme su contraseña'}))

    class Meta:
        """ Metadatos del formulario y validacion de campos """
        model = User # Modelo asociado al formulario
        fields = ['username', 'email', 'nombres', 'apellidos', 'genero', 'password',]

        widgets = {
            'username': forms.TextInput(attrs={'help_text': 'Maximo 12 caracteres.','placeholder': 'Ingrese su nombre de usuario'}),
            'email': forms.EmailInput(attrs={'help_text': 'Ingrese un correo valido.','placeholder': 'Ingrese su correo electronico'}),
            'nombres': forms.TextInput(attrs={'help_text': 'Ingrese sus nombres.','placeholder': 'Ingrese sus nombres'}),
            'apellidos': forms.TextInput(attrs={'help_text': 'Ingrese sus apellidos.','placeholder': 'Ingrese sus apellidos'}),
            'genero': forms.Select(attrs={'help_text': 'Seleccione su genero.'}),
            'password': forms.PasswordInput(attrs={'help_text': 'Ingrese una contraseña segura.', 'placeholder': 'Ingrese su contraseña'}),
        }

    def clean_username(self):
        """ Validar que el nombre de usuario no contenga espacios """
        username = self.cleaned_data.get('username') # Obtener el nombre de usuario
        if ' ' in username: # Verificar si contiene espacios
            raise forms.ValidationError('El nombre de usuario no puede contener espacios.')
        return username

    def clean_email(self):
        """ Validar que el correo electronico sea unico """
        email = self.cleaned_data.get('email') # Obtener el correo electronico
        if User.objects.filter(email=email).exists(): # Verificar si el correo ya existe
            raise forms.ValidationError('El correo electronico ya esta en uso.') # Si existe, lanzar error
        return email # Retornar el correo electronico validado

    def clean_password(self):
        """ Validar que la contraseña tenga al menos 8 caracteres """
        password = self.cleaned_data.get('password') # Obtener la contraseña
        if len(password) < 8: # Verificar la longitud de la contraseña
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return password

    def clean(self):
        cleaned_data = super().clean() # Obtener los datos limpios del formulario
        password = cleaned_data.get('password') # Obtener la contraseña
        password_confirm = cleaned_data.get('password2') # Obtener la confirmacion de la contraseña

        if password and password_confirm: # Verificar que ambas contraseñas coincidan
            if password != password_confirm: # Si no coinciden, lanzar error
                self.add_error('password2', 'Las contraseñas no coinciden.') # Agregar error al campo de confirmacion
        return cleaned_data

    def clean_nombres(self):
        """ Validar que los nombres no contengan numeros """
        nombres = self.cleaned_data.get('nombres') # Obtener los nombres
        if any(char.isdigit() for char in nombres): # Verificar si contienen numeros
            raise forms.ValidationError('Los nombres no pueden contener numeros.') # Si contienen numeros, lanzar error
        return nombres

    def clean_apellidos(self):
        """ Validar que los apellidos no contengan numeros """
        apellidos = self.cleaned_data.get('apellidos')
        if any(char.isdigit() for char in apellidos):
            raise forms.ValidationError('Los apellidos no pueden contener numeros.')
        return apellidos

    def clean_genero(self):
        """ Validar que se haya seleccionado un genero """
        genero = self.cleaned_data.get('genero') # Obtener el genero
        if genero not in dict(User.genero_choice): # Verificar si el genero es valido
            raise forms.ValidationError('Seleccione un genero valido.')
        return genero

    def save(self, commit=True):
        """ Guardar el usuario con la contraseña hasheada """
        user = super().save(commit=False) # Crear el usuario sin guardar
        user.set_password(self.cleaned_data['password']) # Establecer la contraseña hasheada
        if commit: # Guardar el usuario si commit es True
            user.save() # Guardar el usuario en la base de datos
        return user # Retornar el usuario guardado



class CodigoVerificacionForm(forms.Form):
    """ Formulario para verificar el codigo de verificacion """
    # Campos del formulario
    # para recuperar el usuario en la vista.
    username = forms.CharField(
        label='Nombre de Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingrese su nombre de usuario',
            }
        )
    )
    # Campo para el codigo de verificacion
    codigo_verificador = forms.CharField(
        label='Codigo de Verificacion',
        max_length=6,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingrese el codigo de verificacion',
            }
        )
    )

    def clean(self):
        """ Validar el codigo de verificacion """
        cleaned_data = super().clean() # Obtener los datos limpios del formulario
        username = cleaned_data.get('username') # Obtener el nombre de usuario
        codigo_verificador = cleaned_data.get('codigo_verificador') # Obtener el codigo de verificacion del usuario
        # Validar que ambos campos esten completos
        if not username or not codigo_verificador:
            return cleaned_data # Si no, retornar los datos limpios sin mas validacion

        # Verificar si el usuario existe y si el código coincide
        user = User.objects.filter(username=username).first()
        if not user:
            self.add_error('username', 'El usuario no existe.') # Agregar error si el usuario no existe
            return cleaned_data # Retornar los datos limpios
        # Verificar si el código de verificación coincide
        if user.codigo_verificador != codigo_verificador:
            self.add_error('codigo_verificador', 'El código de verificación es incorrecto.')
        # Si todo es correcto, retornar los datos limpios
        return cleaned_data


# No la use....
class UserLoginForm(forms.Form):
    """ Formulario para el login de usuarios """
    # Campos del formulario
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}))

    def clean_username(self):
        """ Validar que el nombre de usuario no contenga espacios """
        username = self.cleaned_data.get('username') # Obtener el nombre de usuario
        if ' ' in username: # Verificar si contiene espacios
            raise forms.ValidationError('El nombre de usuario no puede contener espacios.')
        return username # Retornar el nombre de usuario validado

    def clean_password(self):
        """ Validar que la contraseña tenga al menos 8 caracteres """
        password = self.cleaned_data.get('password') # Obtener la contraseña
        if len(password) < 8: # Verificar la longitud de la contraseña
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return password # Retornar la contraseña validada

    def clean(self):
        """ Validar que el usuario exista """
        cleaned_data = super().clean() # Obtener los datos limpios del formulario
        username = cleaned_data.get('username') # Obtener el nombre de usuario
        password = cleaned_data.get('password') # Obtener la contraseña

        if username and password: # Verificar que ambos campos esten completos
            if not User.objects.filter(username=username).exists(): # Verificar si el usuario existe
                self.add_error('username', 'El nombre de usuario no existe.') # Agregar error si el usuario no existe
            return self.cleaned_data # Retornar los datos limpios



class UpdatePasswordForm(forms.Form):
    """ Formulario para actualizar la contraseña del usuario """

    password_actual = forms.CharField(label='Contraseña Actual',
                                      widget=forms.PasswordInput(attrs={'placeholder': 'contraseña actual'}))
    password_nueva = forms.CharField(label='Nueva Contraseña',
                                     widget=forms.PasswordInput(attrs={'placeholder': 'nueva contraseña'}))
    password_nueva2 = forms.CharField(label='Confirmar Nueva Contraseña',
                                      widget=forms.PasswordInput(attrs={'placeholder': 'Confirme contraseña'}))

    def __init__(self, *args, **kwargs):
        """ Constructor del formulario que recibe el usuario autenticado """
        self.user = kwargs.pop('user')  # Guardamos el usuario autenticado
        super().__init__(*args, **kwargs) # Llamamos al constructor padre


    def clean_password_actual(self):
        """ Validar que la contraseña actual sea correcta """
        password_actual = self.cleaned_data.get('password_actual') # Obtener la contraseña actual

        # Validar que la contraseña actual sea correcta.
        if not self.user.check_password(password_actual):
            raise forms.ValidationError('La contraseña actual es incorrecta.')

        return password_actual # Retornar la contraseña actual validada


    def clean_password_nueva(self):
        """ Validar que la nueva contraseña tenga al menos 8 caracteres """
        password_nueva = self.cleaned_data.get('password_nueva') # Obtener la nueva contraseña
        if len(password_nueva) < 8:
            raise forms.ValidationError('La nueva contraseña debe tener al menos 8 caracteres.')
        return password_nueva # Retornar la nueva contraseña validada

    def clean(self):
        """ Validar coincidencias y que la nueva no sea igual a la anterior """
        cleaned_data = super().clean() # Obtener los datos limpios del formulario
        password_actual = cleaned_data.get('password_actual') # Obtener la contraseña actual
        password_nueva = cleaned_data.get('password_nueva') # Obtener la nueva contraseña
        password_nueva2 = cleaned_data.get('password_nueva2') # Obtener la confirmacion de la nueva contraseña

        # Validar que las nuevas contraseñas coincidan
        if password_nueva and password_nueva2: #  Verificar que ambas nuevas contraseñas coincidan
            if password_nueva != password_nueva2: # Si no coinciden, lanzar error
                self.add_error('password_nueva2', 'Las nuevas contraseñas no coinciden.')

        # Validar que la nueva contraseña no sea igual a la actual
        if password_actual and password_nueva: # Verificar que la nueva contraseña no sea igual a la actual
            if password_actual == password_nueva: # Si son iguales, lanzar error
                self.add_error('password_nueva', 'La nueva contraseña no puede ser igual a la actual.')





