from django.urls import path
from . import views

urlpatterns = [
    path('', views.autenticar, name="autenticar"),
    path('desactivado', views.desactivado, name="no_activo"),
    path('logout', views.desautenticar, name="logout"),
    path('registro', views.RegistrarWizardView.as_view(), name="registrar"),
    path('cambioClave', views.passwordChange, name="passwordChange"),
] 