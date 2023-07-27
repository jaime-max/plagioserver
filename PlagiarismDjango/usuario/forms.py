from django import forms
from modelo.models import Usuario
class FormularioUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["apellidos","nombres","correo"]