from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from modelo.models import Documento, Usuario, GestionDocumentos, Estudiante, Docente
from django.contrib.auth.decorators import login_required
from .forms import FormularioGestion
from django.http import JsonResponse

# Create your views here.
@login_required
def gestionEstudiante (request,gestion_id):
    user = request.user
    usuario_global = Usuario.objects.get(correo=user.email)
    if usuario_global.estado:
        formulario_gestion = FormularioGestion(request.POST)
        if request.method == 'POST':
            if formulario_gestion.is_valid():
                datos_gestion = formulario_gestion.cleaned_data
                #verificar que el email del docente exista
                email_docente = datos_gestion.get('email')
                if Usuario.objects.filter(correo=email_docente).exists():
                    #verificar si el usuario esta registrado como docente
                    print(" ################################################################################## ")
                    print(" verificar si el correo esta asociado a un docente ")
                    print(" ################################################################################## ")
                    usuario = Usuario.objects.get(correo=email_docente)
                    if Docente.objects.filter(usuario = usuario).exists() or user.groups.filter(name = "docente").exists():
                        print("aqui")
                        listaGestion = GestionDocumentos.objects.get (gestion_id = gestion_id)
                        documento = listaGestion.documento

                        listaGestion.titulo = datos_gestion.get('titulo')
                        listaGestion.comentario = datos_gestion.get('comentario')
                        listaGestion.docente = Docente.objects.get(usuario = usuario)
                        listaGestion.save()
                        documento.visible = True
                        documento.save()

                        return render(request, 'gestion/exito.html',locals())
                    else:
                        return HttpResponseRedirect(reverse('homepage'))
                else:
                    return HttpResponseRedirect(reverse('homepage'))
                
            return render(request, 'gestion/gestionEstudiante.html',locals())
        
        return render(request, 'gestion/gestionEstudiante.html',locals())
    else:
        return render(request, 'homepage.html')