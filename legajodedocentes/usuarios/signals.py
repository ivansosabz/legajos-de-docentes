from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from docente.models import Documento


@receiver(post_migrate)
def crear_grupos_roles(sender, **kwargs):
    if sender.name == "usuarios":  # Solo al migrar la app usuarios
        # Grupo Encargado → acceso total
        encargado, _ = Group.objects.get_or_create(name="Encargado")

        # Grupo Asistente → sin permisos de delete y change en Documento
        asistente, _ = Group.objects.get_or_create(name="Asistente")

        # Permisos de modelo Documento
        content_type = ContentType.objects.get_for_model(Documento)
        permisos = Permission.objects.filter(content_type=content_type)

        # Encargado obtiene todos
        encargado.permissions.set(permisos)

        # Asistente obtiene solo add y view
        asistente_permisos = permisos.filter(
            codename__in=["add_documento", "view_documento"]
        )
        asistente.permissions.set(asistente_permisos)

