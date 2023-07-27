import os
import glob
import shutil
from django.shortcuts import render, redirect
from modelo.models import Documento, Usuario, Resultado, GestionDocumentos, Docente, Estudiante
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .nlp.src.python import main


 

# Esta logica solo funciona en la fase de pruebas, en produccion se debe tomar el documento desde la ruta base, en donde se va a cambiar el config para ingresar al
# documento a analizar.
@login_required
def detectar(request, gestion_id):
    user = request.user
    usuario = Usuario.objects.get(correo=user.email)
    if usuario.estado:
        
        gestion = GestionDocumentos.objects.get(gestion_id = gestion_id)
        # documento = Documento.objects.get(documento_id = gestion.documento_id) 
        documento = gestion.documento #ojo
        ruta=os.getcwd()
        new = ruta.replace('\\','/')
        file_path= new +'/plagio/nlp/Test'

        

        ruta_documento_original = documento.archivo.path
        print(os.path)
        archivos_existentes = glob.glob(os.path.join(file_path, '*'))
        for archivo in archivos_existentes:
            os.remove(archivo)
        #Cambio, ya no agregar el documento a la carpeta Test, en cambio enviarla desde la ruta original, cambiar el archivo original 
        nombre_documento = os.path.basename(ruta_documento_original)
        ruta_documento_nuevo = os.path.join(file_path, nombre_documento)
        shutil.copy2(ruta_documento_original, ruta_documento_nuevo)

        resultado = Resultado()
        resultado.documento = documento
        resultado.management = gestion
        resultado.ejecutando = True
        resultado.save()

        documento_generado, nombre= main.main()
        with open(documento_generado, 'rb') as archivo:
            archivo_django = ContentFile(archivo.read(), name=nombre)

        resultado.ejecutando = False
        resultado.archivo.save(nombre, archivo_django)
        resultado.estado = True
        resultado.save()

        return HttpResponseRedirect(reverse('revision', args=[resultado.resultado_id]))
    
    return render(request, 'homepage.html')
    
@login_required
def index(request):
    user = request.user
    usuario = Usuario.objects.get(correo=user.email)
    if usuario.estado:
        if user.groups.filter(name = "docente").exists():
            cond = False
            docente = Docente.objects.get(usuario = usuario)
            listaGestion = GestionDocumentos.objects.filter(docente = docente)
            listaResultado = []
            for gestion in listaGestion:
                try:
                    print(gestion.gestion_id)
                    resultado = Resultado.objects.get(management=gestion)
                    
                    listaResultado.append(resultado)
                    if gestion.estudiante:
                        cond = True
                except Resultado.DoesNotExist:
                     print("el resultado esta procesandose, o no existe en la base de datos")
        elif user.groups.filter(name = "estudiante").exists():
            estudiante = Estudiante.objects.get(usuario = usuario)
            listaGestion = GestionDocumentos.objects.filter(estudiante = estudiante)
            listaResultado = []
            for gestion in listaGestion:
                try:
                    print(gestion.gestion_id)
                    if gestion.docente is not None:
                        resultado = Resultado.objects.get(management=gestion)
                        listaResultado.append(resultado)
                        cond = True
                    else:
                        print('No tiene asignado un profesor para realizar el plagio.')
                except Resultado.DoesNotExist:
                     print("el resultado esta procesandose, o no existe en la base de datos")
            pass
        # busqueda = request.POST.get("busqueda")
        return render (request, 'plagio/index.html', locals())
    return render(request, 'homepage.html')

@login_required
def revision(request,resultado_id):
    #cambio agregar logicca de documento publico 
    user = request.user
    usuario = Usuario.objects.get(correo=user.email)
    if usuario.estado:
        resultado = Resultado.objects.get(resultado_id = resultado_id)
        gestion = GestionDocumentos.objects.get(resultado = resultado)
        return render(request,'plagio/Success.html',locals())
    return