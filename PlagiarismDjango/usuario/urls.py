from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='usuarios'),
    path('crearUsuario', views.crearUsuario, name='crear_usuario'),
    path('eliminarUsuario/<int:usuario_id>/', views.eliminarUsuario, name='eliminar_usuario'),
    path('modificarUsuario/<int:usuario_id>/', views.modificarUsuario, name='modificar_usuario'),
    path('actualizarUsuario', views.actualizarUsuario, name="actualizar_usuario"),
    path('generarUsuario', views.generarUsuario, name="generar_usuario")
    
]