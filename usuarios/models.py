from django.db import models

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, default=3)

    def __str__(self):
        return self.nombre
    
    def is_admin(self):
        return self.id_rol == 1
    
    def is_docente(self):
        return self.id_rol == 2
    
    def is_estudiante(self):
        return self.id_rol == 3
