from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# ────────────────────────────────────────────────
class Carrera(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.nombre)

# ────────────────────────────────────────────────
class NivelDocente(models.Model):
    OPCIONES_NIVEL = [
        ('Encargado', 'Encargado'),
        ('Asistente', 'Asistente'),
        ('Adjunto', 'Adjunto'),
        ('Titular', 'Titular'),
    ]
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=20, choices=OPCIONES_NIVEL)
    anos_requeridos = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

# ────────────────────────────────────────────────
class Docente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    ci = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_ingreso = models.DateField()
    nivel = models.ForeignKey(NivelDocente, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ────────────────────────────────────────────────
class Semestre(models.Model):
    numero = models.PositiveIntegerField()
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Semestre {self.numero} - {self.carrera.nombre if self.carrera else 'Sin carrera'}"

# ────────────────────────────────────────────────
class Materia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.nombre)

# ────────────────────────────────────────────────
class HistorialDocente(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, null=True)
    nivel = models.ForeignKey(NivelDocente, on_delete=models.CASCADE, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.docente.nombre if self.docente else 'Sin docente'} - {self.materia.nombre if self.materia else 'Sin materia'} ({self.fecha_inicio} a {self.fecha_fin or 'actual'})"

# ────────────────────────────────────────────────
class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    nivel = models.ForeignKey(NivelDocente, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.nombre)

# ────────────────────────────────────────────────
class Documento(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField(null=True, blank=True)
    archivo = models.FileField(
        upload_to='documentos/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png', 'doc', 'docx'])],
        null=True,
        blank=True
    )
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.docente.nombre if self.docente else 'Sin docente'}"

# ────────────────────────────────────────────────
class Notificacion(models.Model):
    ESTADO_OPCIONES = [
        ('Pendiente', 'Pendiente'),
        ('Enviado', 'Enviado'),
        ('Renovado', 'Renovado'),
    ]
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, null=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='Pendiente')
    fecha_resolucion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notificación: {self.documento.nombre if self.documento else 'Sin documento'} - {self.estado}"
