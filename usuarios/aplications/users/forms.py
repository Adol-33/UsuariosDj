""" Formularios para la aplicacion de usuarios """

from django import forms
from .models import User

class UserRegisterForm(forms.ModelForm):
    """ Formulario para el registro de usuarios """

    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Confirme su contraseña'}))

    class Meta:
        """ Metadatos del formulario y validacion de campos """
        model = User
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
        username = self.cleaned_data.get('username')
        if ' ' in username:
            raise forms.ValidationError('El nombre de usuario no puede contener espacios.')
        return username
    
    def clean_email(self):
        """ Validar que el correo electronico sea unico """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo electronico ya esta en uso.')
        return email
    
    def clean_password(self):
        """ Validar que la contraseña tenga al menos 8 caracteres """
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password2')

        if password and password_confirm:
            if password != password_confirm:
                self.add_error('password2', 'Las contraseñas no coinciden.')

    def clean_nombres(self):
        """ Validar que los nombres no contengan numeros """
        nombres = self.cleaned_data.get('nombres')
        if any(char.isdigit() for char in nombres):
            raise forms.ValidationError('Los nombres no pueden contener numeros.')
        return nombres
    
    def clean_apellidos(self):
        """ Validar que los apellidos no contengan numeros """
        apellidos = self.cleaned_data.get('apellidos')
        if any(char.isdigit() for char in apellidos):
            raise forms.ValidationError('Los apellidos no pueden contener numeros.')
        return apellidos
    
    def clean_genero(self):
        """ Validar que se haya seleccionado un genero """
        genero = self.cleaned_data.get('genero')
        if genero not in dict(User.genero_choice).keys():
            raise forms.ValidationError('Seleccione un genero valido.')
        return genero
    
    def save(self, commit=True):
        """ Guardar el usuario """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """ Formulario para el login de usuarios """

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}))
    
    def clean_username(self):
        """ Validar que el nombre de usuario no contenga espacios """
        username = self.cleaned_data.get('username')
        if ' ' in username:
            raise forms.ValidationError('El nombre de usuario no puede contener espacios.')
        return username
    
    def clean_password(self):
        """ Validar que la contraseña tenga al menos 8 caracteres """
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return password
    
    def clean(self):
        """ Validar que el usuario exista """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            if not User.objects.filter(username=username).exists():
                self.add_error('username', 'El nombre de usuario no existe.')
            return self.cleaned_data







