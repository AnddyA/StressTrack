from django.urls import path
from . import views

urlpatterns = [
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/eliminar_cuenta/', views.eliminar_usuario, name='eliminar_cuenta'),
    path('perfil/editar_perfil/', views.editar_perfil, name='editar_perfil'),
]
