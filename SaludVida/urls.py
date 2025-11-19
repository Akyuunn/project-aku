# Archivo: SaludVida/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Importamos vistas de login nativas

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Conectamos las rutas de tu aplicación 'gestion'
    path('', include('gestion.urls')),
    
    # Rutas de autenticación (Requerimiento del PDF)
    # Django ya trae el LoginView y LogoutView hechos, solo hay que llamarlos
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]