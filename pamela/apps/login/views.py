from django.views.generic import View
from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.hashers import check_password

from .models import *
from .forms import *

from my_functions import valid_acount # valida si un usuario esta loguiado y tiene cuenta, retorna true/false

from django.http import HttpResponse
# Create your views here.

class Register(View): # vistas del registro de usuario
    #registra un usuario
    def get(self, request):
        if valid_acount(request):
            return redirect(reverse_lazy("login"))
        form = UserCreationForm()
        return render(request, "login/login.html", {"form": form, "title": "Registrarse", "boton_name": "Aceptar"})
    

    def post(self, request):
        
        if valid_acount(request):
            return redirect(reverse_lazy("login"))
        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            user = authenticate(request=request, username=usuario.username, password=form.cleaned_data['password1'])
            if user is not None:
                # Establecer la sesión de usuario
                login(request, user)
                return redirect(reverse_lazy("acount"))
        
        content = {
            "form": UserCreationForm(request.POST),
            "title": "Registro",
            "boton_name": "Aceptar"
            }

        return render(request, "login/login.html", content)

def user_logout(request):
    logout(request)
    return redirect(reverse_lazy("login"))

def register_acount(request): # registra una ceunta vinculada a un usuario de auth_user
    if request.user.is_authenticated: # si esta autenticado
        if not valid_acount(request):    # no tiene una cuenta
            if request.method == "POST":
                form = AcountForm(request.POST)
                if form.is_valid():
                    new_acount = form.save(commit=False)
                    new_acount.user = request.user  # Asigna el usuario actualmente autenticado
                    new_acount.save()  # Ahora guarda la instancia con el usuario asignado

                    # Actualiza el correo electrónico en la tabla auth_user con el valor de Acount
                    request.user.email = new_acount.email
                    request.user.save()

                    return redirect(reverse_lazy('turns'))  
                else:
                    form = AcountForm(request.POST)
            else:
                form = AcountForm()

            context = {
                "form": form,
                "title": "Registro",
                "boton_name": "Acptar"
                }
            return render(request, "login/login.html", context)

    return redirect(reverse_lazy("register"))


def view_login(request): # la vista del login
    if valid_acount(request): # si el usuario esta logueado y tiene cuenta
            return redirect(reverse_lazy('turns'))
    #autenticacion de usuario
    content = {"title": "Iniciar sesion", "boton_name": "Login"}
    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']  
            password = form.cleaned_data['password']
            
            # Busca el usuario por correo electrónico
            user = User.objects.get(email=email)
            
            if user is not None and check_password(password, user.password):
                authenticated_user = authenticate(request, username=user.username, password=password)
                login(request, authenticated_user)
                return redirect(reverse_lazy('turns'))
            else:
                content = {"msj": "Usuario o contraseña incorrecta"}
    #quitar
    user = User.objects.get(id=1)
    form = LoginForm(initial={'email': user.email})
    #form = LoginForm()
    content["form"] = form
    return render(request, "login/login.html", content)



