from django.db import models

# Modelo Medico según tabla del PDF [cite: 59]
class Medico(models.Model):
    # Requisito: Mínimo dos palabras, tres letras cada una (se validará en forms.py)
    nombre_completo = models.CharField(max_length=200)
    # Requisito: Formato chileno válido
    rut = models.CharField(max_length=12)
    # Requisito: Ej: Pediatría, Cardiología
    especialidad = models.CharField(max_length=100)
    # Requisito: Único
    correo = models.EmailField(unique=True)
    # Requisito: Opcional
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_completo} ({self.especialidad})"

# Modelo Paciente según tabla del PDF [cite: 60-75]
class Paciente(models.Model):
    OPCIONES_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    nombre_completo = models.CharField(max_length=200)
    rut = models.CharField(max_length=12)
    # Requisito: Obligatorio
    fecha_nacimiento = models.DateField()
    # Requisito: 'M', 'F', 'O'
    sexo = models.CharField(max_length=1, choices=OPCIONES_SEXO)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_completo} - {self.rut}"

# Modelo Cita según tabla del PDF [cite: 76]
class Cita(models.Model):
    # Requisito: Relación con Paciente (Obligatorio)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    # Requisito: Relación con Médico (Obligatorio)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    # Requisito: Debe coincidir con la especialidad del médico
    especialidad = models.CharField(max_length=100)
    # Requisito: No puede ser anterior a hoy (se valida en forms.py)
    fecha_cita = models.DateField()
    # Requisito: Validar disponibilidad (se valida en forms.py)
    hora_cita = models.TimeField()
    # Requisito: Opcional
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cita: {self.paciente} con {self.medico} el {self.fecha_cita}"