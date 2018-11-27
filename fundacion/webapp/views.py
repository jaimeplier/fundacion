from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse


def login(request):
    error_message = ''
    context = {}
    if request.method == 'POST':
        email = request.POST['correo']
        password = request.POST['password']
        user = authenticate(correo=email, password=password)
        if user is not None:
            auth_login(request, user)
            if request.POST.get('next') is not None:
                return redirect(request.POST.get('next'))
            elif user.rol.nombre == 'administrador':
                return redirect(reverse('administrador:index'))
            elif user.rol.nombre == 'directorio':
                return redirect(reverse('administrador:list_acude_institucion'))
            elif user.rol.nombre == 'consejero':
                return redirect(reverse('administrador:index'))
            elif user.rol.nombre == 'supervisor':
                return redirect(reverse('administrador:index'))
            elif user.rol.nombre == 'calidad':
                return redirect(reverse('administrador:index'))
            return redirect(reverse('administrador:index'))
        else:
            error_message = "Usuario y/o contraseña incorrectos"
            context = {
                'error_message': error_message, 'next': request.POST.get('next')
            }
            return render(request, 'config/login.html', context)
    if request.GET.get('next') is not None:
        context['next'] = request.GET.get('next')
    return render(request, 'config/login.html', context)
