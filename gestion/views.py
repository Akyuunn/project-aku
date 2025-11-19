from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medico, Paciente, Cita
from .forms import MedicoForm, PacienteForm, CitaForm

# --- PÁGINA DE INICIO ---
def inicio(request):
    return render(request, 'index.html')

# --- GESTIÓN DE MÉDICOS ---

@login_required
def lista_medicos(request):
    medicos = Medico.objects.all()
    return render(request, 'lista_medicos.html', {'medicos': medicos})

@login_required
def crear_medico(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médico registrado correctamente.')
            return redirect('lista_medicos')
    else:
        form = MedicoForm()
    return render(request, 'form_medico.html', {'form': form, 'titulo': 'Registrar Médico'})

@login_required
def editar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos del médico actualizados.')
            return redirect('lista_medicos')
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'form_medico.html', {'form': form, 'titulo': 'Editar Médico'})

@login_required
def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    medico.delete()
    messages.success(request, 'Médico eliminado del sistema.')
    return redirect('lista_medicos')

# ==========================================
# GESTIÓN DE PACIENTES (CRUD)
# ==========================================

@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    # Tu colega debe crear 'lista_pacientes.html'
    return render(request, 'lista_pacientes.html', {'pacientes': pacientes})

@login_required
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente registrado correctamente.')
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    # Tu colega debe crear 'form_paciente.html'
    return render(request, 'form_paciente.html', {'form': form, 'titulo': 'Registrar Paciente'})

@login_required
def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado.')
            return redirect('lista_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'form_paciente.html', {'form': form, 'titulo': 'Editar Paciente'})

@login_required
def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    paciente.delete()
    messages.success(request, 'Paciente eliminado.')
    return redirect('lista_pacientes')

# ==========================================
# GESTIÓN DE CITAS MÉDICAS (CRUD + BUSCADOR)
# ==========================================

@login_required
def lista_citas(request):
    # Lógica del BUSCADOR AVANZADO (Requisito del PDF )
    citas = Cita.objects.all().order_by('fecha_cita', 'hora_cita')
    
    # Capturamos los filtros de la URL (GET)
    medico_id = request.GET.get('medico')
    paciente_id = request.GET.get('paciente')
    fecha = request.GET.get('fecha')

    if medico_id:
        citas = citas.filter(medico_id=medico_id)
    if paciente_id:
        citas = citas.filter(paciente_id=paciente_id)
    if fecha:
        citas = citas.filter(fecha_cita=fecha)

    # Enviamos también las listas para llenar los selectores del filtro en el HTML
    medicos = Medico.objects.all()
    pacientes = Paciente.objects.all()

    context = {
        'citas': citas,
        'medicos': medicos,
        'pacientes': pacientes
    }
    # Tu colega debe crear 'lista_citas.html'
    return render(request, 'lista_citas.html', context)

@login_required
def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita agendada exitosamente.')
            return redirect('lista_citas')
        else:
            messages.error(request, 'Error al agendar. Revise las reglas de negocio.')
    else:
        form = CitaForm()
    return render(request, 'form_cita.html', {'form': form, 'titulo': 'Agendar Nueva Cita'})

@login_required
def editar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita modificada.')
            return redirect('lista_citas')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'form_cita.html', {'form': form, 'titulo': 'Modificar Cita'})

@login_required
def eliminar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    cita.delete()
    messages.success(request, 'Cita cancelada/eliminada.')
    return redirect('lista_citas')