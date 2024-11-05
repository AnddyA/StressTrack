from django.shortcuts import render, redirect
from .forms import RegistroForm, UsuarioForm
from django.urls import reverse_lazy
from .models import Usuario
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import update_session_auth_hash


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


def perfil(request):
    usuario = request.user  # Obtiene el usuario actual

    if request.method == 'POST':
        # Si el usuario desea actualizar su perfil
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        
        # Actualiza los datos del usuario
        if nombre:
            usuario.username = nombre
        if correo:
            usuario.email = correo
        if contrasena:
            usuario.set_password(contrasena)
        usuario.save()

        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('usuario:perfil')

    return render(request, 'perfil.html', {'usuario': usuario})

def editar_perfil(request):
    """Permite al usuario actualizar su nombre, correo y contraseña"""
    usuario = request.user

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        # Actualiza los campos según los datos recibidos
        if nombre:
            usuario.username = nombre
        if correo:
            usuario.email = correo
        if contrasena:
            usuario.set_password(contrasena)
            # Actualiza la sesión para que el usuario no tenga que volver a iniciar sesión
            update_session_auth_hash(request, usuario)

        usuario.save()
        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('usuarios:perfil_usuario')  # Redirige a la página de perfil

    # Si no es POST, renderiza la página de edición de perfil
    return render(request, 'usuarios/editar_perfil.html', {'usuario': usuario})