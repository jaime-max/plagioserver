from django.urls import path
from . import views

urlpatterns = [
    path('detectar/<int:gestion_id>/', views.detectar, name='detectar'),
    path('', views.index, name='resultados'),
    path('revision/<int:resultado_id>/', views.revision, name='revision')
    # path('visualizar/<int:documento_id>/', views.visualizar_archivo, name='visualizar_archivo'),
]
