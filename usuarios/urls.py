from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/eliminar/<int:usuario_id>/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('perfil/editar/<int:usuario_id>/', views.editar_perfil, name='editar_perfil'),
]
