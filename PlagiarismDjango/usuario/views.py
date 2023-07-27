from django.shortcuts import render
from modelo.models import Usuario
from .forms import FormularioUsuario
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User  
from django.db.models import Q 
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

# @login_required
def index(request):
    user = request.user
    usuarioGuardado = User.objects.get(email = user.email)
    cond = usuarioGuardado.first_name.strip() # valor de la variable first_name
    cond = not cond # mandar true si esta vacio 
    # if user.groups.filter(name = "gestion_aereopuerto").exists():
    listaUsuarios = Usuario.objects.all() 
    busqueda = request.POST.get("busqueda")
    if busqueda:
        listaUsuarios = Usuario.objects.filter(
            Q(apellidos__icontains = busqueda) | 
            Q(nombres__icontains = busqueda) 
        ).distinct() 
    return render (request, 'usuarios/index_Todos.html', locals())
    # else:
    #     return render(request, 'login/forbidden.html', locals()) 


# @login_required
def crearUsuario(request):
    user = request.user
    # if user.groups.filter(name = "gestion_aereopuerto" ).exists() and user.has_perm('usuario.add_usuario'):
    #     formulario_usuario = FormularioUsuario(request.POST)
    #     if request.method == 'POST':
    #         if formulario_usuario.is_valid():
    #             usuario = Usuario()
    #             datos_usuario = formulario_usuario.cleaned_data
    #             usuario.apellidos= datos_usuario.get('apellidos')
    #             usuario.nombres= datos_usuario.get('nombres')
    #             usuario.correo= datos_usuario.get('correo')
                
    #                 #ORM
            
    #             usuario.save()
            
    #         return redirect(index)
    #     return render (request, 'usuarios/crear.html', locals())
    # else:
    #     return render(request, 'login/forbidden.html', locals()) 

def eliminarUsuario(request, usuario_id):
    user = request.user
    # if user.groups.filter(name = "gestion_aereopuerto").exists():
    #     usuario = Usuario.objects.get(usuario_id=id)
    #     usuario.delete()
    #     return redirect(index)
    # else:
    #     return render(request, 'login/forbidden.html', locals())

def modificarUsuario(request, usuario_id):
    user = request.user
    # if user.groups.filter(name = "gestion_aereopuerto").exists():
    usuario = Usuario.objects.get(usuario_id=usuario_id)
    if request.method == 'GET':
        formulario_usuario = FormularioUsuario(instance = usuario)
    else:
        formulario_usuario = FormularioUsuario(request.POST, instance = usuario)
        if formulario_usuario.is_valid():
            #ORM
            formulario_usuario.save()
        return redirect(index)
    return render (request, 'usuarios/modificar.html', locals())
    # else:
    #     return render(request, 'login/forbidden.html', locals())

def actualizarUsuario(request): 
    user = request.user
    # if user.groups.filter(name = "Usuario").exists():   #@login_required
    #     email = user.email
    #     usuario = Usuario.objects.get(correo=email)
    #     if request.method == 'GET':
    #         formulario_usuario = FormularioUsuario(instance = usuario)
    #     else:
    #         formulario_usuario = FormularioUsuario(request.POST, instance = usuario)
    #         if formulario_usuario.is_valid():
    #             #ORM
    #             formulario_usuario.save()
    #         #return HttpResponseRedirect(reverse('viajes'))
    #     return render (request, 'Usuarios/modificar.html', locals())
    # else:
    #     return render(request, 'login/forbidden.html', locals())

def generarUsuario(request):
    user = request.user
    formulario_usuario = FormularioUsuario(request.POST)
    if request.method == 'POST':
        if formulario_usuario.is_valid():
            usuario = Usuario()
            datos_usuario = formulario_usuario.cleaned_data
            usuario.apellidos= datos_usuario.get('apellidos')
            usuario.nombres= datos_usuario.get('nombres')
            usuario.correo= user.email
            usuarioGuardado = User.objects.get(email = user.email)
            usuarioGuardado.first_name = usuario.nombres
            usuarioGuardado.last_name = usuario.apellidos
            
                #ORM
            usuario.save()
            usuarioGuardado.save()
        return redirect(index)
    return render (request, 'usuarios/crear.html', locals())
    