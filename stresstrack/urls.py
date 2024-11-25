"""
URL configuration for stresstrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from usuarios import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('register/', views.register, name='register'),


    path('administrador/', views.administrador_index, name='administrador_index'),

    path('administrador/usuarios/', views.administrador_usu, name='administrador_usu'),
    path('administrador/usuarios/crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('administrador/usuarios/editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('administrador/usuarios/eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('docente/', views.docente_index, name='docente_index'),

    path('estudiante/', views.estudiante_index, name='estudiante_index'),


    path('usuario/', include('usuarios.urls')),
    
    path('superadmin/', admin.site.urls),
]
