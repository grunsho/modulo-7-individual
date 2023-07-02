from django.contrib.auth.forms import forms
from .models import Usuario

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, label='Nombre de Usuario', error_messages={
        'required': 'El nombre de usuario es obligatorio'})
    password = forms.CharField(max_length=16, required=True, label='Contraseña',
        widget=forms.PasswordInput, error_messages={'required': 'La contraseña es obligatoria'})
    class Meta:
        model = Usuario