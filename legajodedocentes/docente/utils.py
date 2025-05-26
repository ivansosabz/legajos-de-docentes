
from datetime import date
from .models import Documento, Notificacion

def generar_notificaciones_vencidas():
    hoy = date.today()
    documentos_vencidos = Documento.objects.filter(
        fecha_vencimiento__lt=hoy,
        fecha_vencimiento__isnull=False
    )

    for doc in documentos_vencidos:
        ya_notificado = Notificacion.objects.filter(
            documento=doc,
            estado='Pendiente'
        ).exists()
        if not ya_notificado:
            Notificacion.objects.create(
                docente=doc.docente,
                documento=doc,
                estado='Pendiente'
            )