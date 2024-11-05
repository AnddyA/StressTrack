from django.shortcuts import render, redirect
from .forms import RegistroForm, UsuarioForm
from django.urls import reverse_lazy
from .models import Usuario
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import login, authenticate

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Porfavor, inicia sesión")
            print("todo bien")
            return redirect('login')  # Redirige a la página de login
        else:
            messages.error(request, "Error en el registro. Verfica los datos e intenta nuevamente")
            print("todo maso mal")
    else:
        form = RegistroForm()
        print("todo mal")
    return render(request, 'register.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                if user.is_admin():
                    return redirect('admin_dashboard')
                elif user.is_docente():
                    return redirect('docente_dashboard')
                elif user.is_estudiante():
                    return redirect('estudiante_dashboard')
    else:
        form = UsuarioForm()
    return render(request, 'login.html', {'form': form})

'''
def login_usuario(request):
    if request.method == 'POST':
        print("no")
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Usuario.objects.get(email=email)
            if check_password(password, user.password): # Verifica la contraseña
                if user.id_rol == 1:
                    print("ingreso de admin")
                    return redirect('administrador_dashboard')
                elif user.id_rol == 2:
                    print("ingreso de docente")
                    return redirect('docente_dashboard')
                elif user.id_rol == 3:
                    print("ingreso de estud")
                    return redirect('estudiante_dashboard')
            else:
                return render(request, 'login.html', {'error': 'Credenciales inválidas'})
                print("nosirven")
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
            print("noexiste")
    return render(request, 'login.html')
    print("noentro")
'''
def administrador_dashboard(request):
    usuarios = Usuario.objects.all()
    return render(request, 'administrador_dashboard.html', {'usuarios':usuarios})

def docente_dashboard(request):
    return render(request, 'docente_dashboard.html')

def estudiante_dashboard(request):
    return render(request, 'estudiante_dashboard.html')


def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrador_dashboard')
    else:
        form = UsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})

def editar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('administrador_dashboard')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})

def eliminar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    usuario.delete()
    return redirect('administrador_dashboard')

def logout(request):
    return redirect(request, 'logout.html')

def perfil(request):
    return redirect(request, 'perfil.html')