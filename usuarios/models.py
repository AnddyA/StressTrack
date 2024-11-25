from django.db import models

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    dni = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, default=3)#Rol1=Administrador, Rol2=Docente, Rol3=Estudiante

    def __str__(self):
        return self.nombre
