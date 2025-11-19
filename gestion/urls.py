from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    # Médicos
    path('medicos/', views.lista_medicos, name='lista_medicos'),
    path('medicos/crear/', views.crear_medico, name='crear_medico'),
    path('medicos/editar/<int:id>/', views.editar_medico, name='editar_medico'),
    path('medicos/eliminar/<int:id>/', views.eliminar_medico, name='eliminar_medico'),

    # Pacientes
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/eliminar/<int:id>/', views.eliminar_paciente, name='eliminar_paciente'),

    # Citas (Incluye el buscador en la lista)
    path('citas/', views.lista_citas, name='lista_citas'),
    path('citas/crear/', views.crear_cita, name='crear_cita'),
    path('citas/editar/<int:id>/', views.editar_cita, name='editar_cita'),
    path('citas/eliminar/<int:id>/', views.eliminar_cita, name='eliminar_cita'),
]