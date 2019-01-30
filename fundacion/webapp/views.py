from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

def index(request):
    template_name = 'config/index.html'
    return render(request, template_name)

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
                return redirect(reverse('webapp:index'))
            elif user.rol.nombre == 'directorio':
                return redirect(reverse('directorio:list_acude_institucion'))
            elif user.rol.nombre == 'consejero':
                return redirect(reverse('consejero:registro_primera_vez'))
            elif user.rol.nombre == 'supervisor':
                return redirect(reverse('supervisor:resumen'))
            elif user.rol.nombre == 'calidad':
                return redirect(reverse('calidad:list_evaluacion'))
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

def logout_view(request):
    logout(request)
    return redirect(reverse('webapp:login'))
