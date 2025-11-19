from django import forms
from .models import Medico, Paciente, Cita
from django.utils import timezone
import datetime

# --- VALIDACIÓN DE NOMBRE (Reutilizable) ---
def validar_nombre_completo(nombre):
    """
    Regla de negocio: Los nombres deben tener al menos dos palabras,
    cada una de al menos tres letras[cite: 35, 55].
    """
    palabras = nombre.strip().split()
    
    if len(palabras) < 2:
        raise forms.ValidationError("El nombre debe tener al menos dos palabras (Nombre y Apellido).")
    
    for palabra in palabras:
        if len(palabra) < 3:
            raise forms.ValidationError(f"La palabra '{palabra}' es muy corta. Mínimo 3 letras.")
    
    return nombre

# --- FORMULARIO DE MÉDICO ---
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = '__all__'
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Pérez'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get('nombre_completo')
        return validar_nombre_completo(nombre)

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        # Aquí podríamos agregar el algoritmo de Módulo 11 si lo necesitas después.
        # Por ahora verificamos que tenga guion.
        if '-' not in rut:
            raise forms.ValidationError("El RUT debe incluir el guion (Ej: 12345678-9).")
        return rut

# --- FORMULARIO DE PACIENTE ---
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), # Selector de fecha HTML5
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get('nombre_completo')
        return validar_nombre_completo(nombre)

# --- FORMULARIO DE CITA (El más importante) ---
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        widgets = {
            'fecha_cita': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_cita': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_fecha_cita(self):
        fecha = self.cleaned_data.get('fecha_cita')
        # Regla: Las citas no pueden ser agendadas para fechas anteriores al día actual[cite: 31, 42].
        if fecha and fecha < timezone.now().date():
            raise forms.ValidationError("No se pueden agendar citas en el pasado.")
        return fecha

    def clean(self):
        """Validaciones cruzadas entre campos (Reglas de Negocio complejas)"""
        cleaned_data = super().clean()
        medico = cleaned_data.get('medico')
        fecha = cleaned_data.get('fecha_cita')
        hora = cleaned_data.get('hora_cita')
        paciente = cleaned_data.get('paciente')
        especialidad = cleaned_data.get('especialidad')

        # Si faltan datos básicos, no validamos lógica compleja
        if not (medico and fecha and hora and paciente and especialidad):
            return

        # Regla: Un médico no puede tener dos citas asignadas en el mismo horario[cite: 34, 54].
        citas_medico = Cita.objects.filter(medico=medico, fecha_cita=fecha, hora_cita=hora)
        if self.instance.pk: # Si estamos editando, nos excluimos a nosotros mismos
            citas_medico = citas_medico.exclude(pk=self.instance.pk)
        
        if citas_medico.exists():
            self.add_error('hora_cita', "Este médico ya tiene una cita asignada a esa hora.")

        # Regla: Un paciente no puede tener más de una cita el mismo día en la misma especialidad[cite: 33, 53].
        citas_paciente = Cita.objects.filter(paciente=paciente, fecha_cita=fecha, especialidad__iexact=especialidad)
        if self.instance.pk:
            citas_paciente = citas_paciente.exclude(pk=self.instance.pk)

        if citas_paciente.exists():
            self.add_error('especialidad', "El paciente ya tiene una cita de esta especialidad para hoy.")
        
        # Validación extra sugerida: Especialidad debe coincidir con la del médico[cite: 49].
        if especialidad.lower() != medico.especialidad.lower():
            self.add_error('especialidad', f"La especialidad no coincide. El médico es: {medico.especialidad}")

        return cleaned_data