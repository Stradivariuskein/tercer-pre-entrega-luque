from .models import Acount
from django import forms
from django.contrib.auth.models import User # user por defecto django


class AcountForm(forms.ModelForm):
    date = forms.DateField()
    class Meta:
        model = Acount
        fields = ('email', 'name', 'lastName', 'date', 'phone')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Usar PasswordInput para ocultar la contraseña

    class Meta:
        model = User
        fields = ('email', 'password')

