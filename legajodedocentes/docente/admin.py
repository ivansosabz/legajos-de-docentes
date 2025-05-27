
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from docente.models import Carrera, NivelDocente, Docente, Semestre, Materia, HistorialDocente, TipoDocumento, \
    Documento, Notificacion


class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


class NivelDocenteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'anos_requeridos')
    list_filter = ('nombre',)
    search_fields = ('codigo', 'nombre')
    ordering = ('anos_requeridos',)


class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'ci', 'email', 'telefono', 'nivel', 'fecha_ingreso')
    list_filter = ('nivel', 'fecha_ingreso')
    search_fields = ('nombre', 'apellido', 'ci', 'email')
    ordering = ('apellido', 'nombre')
    date_hierarchy = 'fecha_ingreso'
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'ci')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono')
        }),
        ('Información Laboral', {
            'fields': ('fecha_ingreso', 'nivel')
        }),
    )

    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"

    nombre_completo.short_description = 'Nombre Completo'


class SemestreAdmin(admin.ModelAdmin):
    list_display = ('numero', 'carrera')
    list_filter = ('carrera',)
    search_fields = ('numero', 'carrera__nombre')
    ordering = ('carrera', 'numero')


class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'semestre', 'carrera')
    list_filter = ('semestre__carrera', 'semestre')
    search_fields = ('nombre', 'semestre__numero')
    ordering = ('nombre',)

    def carrera(self, obj):
        return obj.semestre.carrera if obj.semestre else None

    carrera.short_description = 'Carrera'


class HistorialDocenteAdmin(admin.ModelAdmin):
    list_display = ('docente', 'materia', 'nivel', 'fecha_inicio', 'fecha_fin', 'duracion')
    list_filter = ('nivel', 'materia__semestre__carrera')
    search_fields = ('docente__nombre', 'docente__apellido', 'materia__nombre')
    date_hierarchy = 'fecha_inicio'

    def duracion(self, obj):
        if obj.fecha_fin:
            return f"{(obj.fecha_fin - obj.fecha_inicio).days} días"
        return "En curso"

    duracion.short_description = 'Duración'


class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel')
    list_filter = ('nivel',)
    search_fields = ('nombre', 'nivel__nombre')
    ordering = ('nivel', 'nombre')


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'docente', 'tipo_documento', 'fecha_emision', 'fecha_vencimiento', 'estado',
                    'ver_archivo')
    list_filter = ('tipo_documento', 'docente__nivel')
    search_fields = ('nombre', 'docente__nombre', 'docente__apellido')
    date_hierarchy = 'fecha_emision'
    readonly_fields = ('estado',)
    actions = ['marcar_como_vencido']

    def estado(self, obj):
        hoy = timezone.now().date()
        if obj.fecha_vencimiento:
            if obj.fecha_vencimiento < hoy:
                return format_html('<span style="color: red;">Vencido</span>')
            elif (obj.fecha_vencimiento - hoy).days <= 30:
                return format_html('<span style="color: orange;">Por vencer</span>')
        return format_html('<span style="color: green;">Vigente</span>')

    estado.short_description = 'Estado'

    def ver_archivo(self, obj):
        if obj.archivo:
            return format_html('<a href="{}" target="_blank">Ver</a>', obj.archivo.url)
        return "Sin archivo"

    ver_archivo.short_description = 'Archivo'

    def marcar_como_vencido(self, request, queryset):
        queryset.update(fecha_vencimiento=timezone.now().date() - timezone.timedelta(days=1))

    marcar_como_vencido.short_description = "Marcar como vencido"


class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('docente', 'documento', 'fecha_envio', 'estado', 'fecha_resolucion')
    list_filter = ('estado', 'fecha_envio')
    search_fields = ('docente__nombre', 'docente__apellido', 'documento__nombre')
    date_hierarchy = 'fecha_envio'
    readonly_fields = ('fecha_envio',)
    actions = ['marcar_como_enviadas']

    def marcar_como_enviadas(self, request, queryset):
        queryset.update(estado='Enviado', fecha_resolucion=timezone.now())

    marcar_como_enviadas.short_description = "Marcar como enviadas"


# Registro de modelos con sus clases admin personalizadas
admin.site.register(Carrera, CarreraAdmin)
admin.site.register(NivelDocente, NivelDocenteAdmin)
admin.site.register(Docente, DocenteAdmin)
admin.site.register(Semestre, SemestreAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(HistorialDocente, HistorialDocenteAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Notificacion, NotificacionAdmin)