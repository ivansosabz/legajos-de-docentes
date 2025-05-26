from django.contrib import admin
from docente.models import Carrera, NivelDocente, Docente, Semestre, Materia, HistorialDocente, TipoDocumento, Documento, Notificacion

admin.site.register(Carrera)
admin.site.register(NivelDocente)
admin.site.register(Docente)
admin.site.register(Semestre)
admin.site.register(Materia)
admin.site.register(HistorialDocente)
admin.site.register(TipoDocumento)
admin.site.register(Documento)
admin.site.register(Notificacion)
