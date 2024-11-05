from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario, Rol

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(user.password)  # Hashear la contraseña
        user.id_rol = Rol.objects.get(id=3)  # ID para rol de Estudiante
        if commit:
            user.save()
        return user

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'password', 'id_rol']
