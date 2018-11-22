from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse


def login(request):
    error_message = ''
    context = {}
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']
        usuario = User.objects.filter(email=correo)
        if usuario.exists():
            username = usuario.first().username
        else:
            error_message = "Usuario y/o contraseña incorrectos"
            context = {
                'error_message': error_message, 'next': request.POST.get('next')
            }
            return render(request, 'config/login.html', context)
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            for p in user.user_permissions.all():
                print(p)
            if request.POST.get('next') is not None:
                return redirect(request.POST.get('next'))
            elif user.user_permissions.filter(codename='administrador').exists():
                return redirect(reverse('administrador:index'))
            elif user.user_permissions.filter(codename='directorio').exists():
                return redirect(reverse('administrador:list_acude_institucion'))
            elif user.user_permissions.filter(codename='consejero').exists():
                return redirect(reverse('administrador:index'))
            elif user.user_permissions.filter(codename='supervisor').exists():
                return redirect(reverse('administrador:index'))
            elif user.user_permissions.filter(codename='calidad').exists():
                return redirect(reverse('administrador:index'))
            return redirect(reverse('webapp:index'))
        else:
            error_message = "Usuario y/o contraseña incorrectos"
            context = {
                'error_message': error_message, 'next': request.POST.get('next')
            }
            return render(request, 'config/login.html', context)
    if request.GET.get('next') is not None:
        context['next'] = request.GET.get('next')
    return render(request, 'config/login.html', context)

