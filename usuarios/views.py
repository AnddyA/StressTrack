from django.shortcuts import render, redirect
from .forms import RegistroForm, UsuarioForm
from django.urls import reverse_lazy
from .models import Usuario, Rol
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
def index(request):
    return render(request, 'inicio/index.html')

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Porfavor, inicia sesión")
            return redirect('index')
        else:
            messages.error(request, "Error en el registro. Verfica los datos e intenta nuevamente")
    else:
        form = RegistroForm()
    return render(request, 'inicio/index.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Usuario.objects.get(email=email)
            if password == user.password:  # Compara la contraseña sin cifrar
                messages.success(request, "Inicio de sesión exitoso")
                if user.id_rol.nombre_rol == 'Administrador':
                    return redirect('administrador_index')
                elif user.id_rol.nombre_rol == 'Docente':
                    return redirect('docente_index')
                elif user.id_rol.nombre_rol == 'Estudiante':
                    return redirect('estudiante_index')
            else:
                return render(request, 'inicio/index.html', {'error': 'Credenciales inválidas'})
        except Usuario.DoesNotExist:
            return render(request, 'inicio/index.html', {'error': 'Credenciales inexistentes'})
    return render(request, 'inicio/index.html')

def administrador_index(request):
    usuarios = Usuario.objects.all()
    return render(request, 'admin/indexA.html', {'usuarios':usuarios})

def administrador_usu(request):
    usuarios = Usuario.objects.all()
    return render(request, 'admin/usuarioG.html', {'usuarios':usuarios})

def docente_index(request):
    return render(request, 'docente/indexD.html')

def estudiante_index(request):
    return render(request, 'estudiante/indexE.html')


def crear_usuario(request):
    roles = Rol.objects.all()

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrador_usu')
        else:
            messages.error(request, "Error en el registro. Verfica los datos e intenta nuevamente")
    else:
        form = UsuarioForm()
    return render(request, 'admin/usuarioG.html', {'form': form, 'roles': roles} )

def editar_usuario(request, usuario_id):
    roles = Rol.objects.all()
    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('administrador_usu')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'admin/editar_usuario.html', {'form': form, 'usuario': usuario, 'roles': roles})

def eliminar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    usuario.delete()
    return redirect('administrador_usu')

def eliminar_cuenta(request, usuario_id):

    usuario = Usuario.objects.get(id=usuario_id)
    usuario.delete()
    return render(request, 'inicio/index.html', {usuario:usuario_id})


def perfil(request):
    usuario = request.user  # Obtiene el usuario actual autenticado
    return render(request, 'inicio/perfil.html', {'user': usuario})


def editar_perfil(request):

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
        return redirect('perfil')  # Redirige a la página de perfil

    # Si no es POST, renderiza la página de edición de perfil
    return render(request, 'usuarios/editar_perfil.html', {'user': usuario})