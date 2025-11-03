from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agregar/', views.agregar_monitor, name='agregar_monitor'),
    path('comparar/', views.comparar_monitores, name='comparar_monitores'),
    path('comprar/<int:monitor_id>/', views.comprar_monitor, name='comprar_monitor'),
    path('buscar/', views.buscar_monitor, name='buscar_monitor'),
    path('login/', auth_views.LoginView.as_view(template_name='instrumentos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('monitor/<int:monitor_id>/', views.detalle_monitor, name='detalle_monitor'),
]