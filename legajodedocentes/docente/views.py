from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone

from .forms import DocenteForm, DocumentoForm
from .models import Docente, Documento, Notificacion
from datetime import date
from .utils import generar_notificaciones_vencidas

# ------------------ DOCENTES ------------------

def index(request):
    query = request.GET.get('search', '')
    docentes = Docente.objects.filter(
        Q(nombre__icontains=query) |
        Q(apellido__icontains=query) |
        Q(ci__icontains=query) |
        Q(nivel__nombre__icontains=query)
    )
    return render(request, 'docentes/index.html', {'docentes': docentes})

def view(request, id):
    docente = get_object_or_404(Docente, id=id)
    return render(request, 'docentes/details.html', {'docente': docente})

def create(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Docente agregado correctamente.')
            return redirect('docente')
        else:
            messages.error(request, 'Hubo un error al agregar el docente. Revisa los campos.')
    else:
        form = DocenteForm()

    return render(request, 'docentes/create.html', {'form': form})

def edit(request, id):
    docente = get_object_or_404(Docente, id=id)

    if request.method == 'POST':
        form = DocenteForm(request.POST, instance=docente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Docente actualizado correctamente.')
        else:
            messages.error(request, 'Revisá los errores del formulario.')
    else:
        form = DocenteForm(instance=docente)

    return render(request, 'docentes/edit.html', {'form': form, 'id': id})

@require_POST
def delete(request, id):
    docente = get_object_or_404(Docente, id=id)
    docente.delete()
    messages.success(request, 'Docente eliminado correctamente.')
    return redirect('docente')

# ------------------ DOCUMENTOS ------------------

def documento(request):
    query = request.GET.get('search', '')
    documentos = Documento.objects.filter(
        Q(nombre__icontains=query) |
        Q(docente__nombre__icontains=query) |
        Q(docente__apellido__icontains=query) |
        Q(docente__ci__icontains=query) |
        Q(tipo_documento__nombre__icontains=query)
    )
    return render(request, 'documentos/index.html', {'documentos': documentos})

def create_document(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento agregado correctamente.')
            return redirect('documento')
        else:
            messages.error(request, 'Hubo un error al agregar el documento. Revisa los campos.')
    else:
        form = DocumentoForm()

    return render(request, 'documentos/create.html', {'form': form})

def edit_document(request, id):
    documento = get_object_or_404(Documento, id=id)
    fecha_anterior = documento.fecha_vencimiento  # Guardamos la fecha antes de editar

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            nuevo_doc = form.save()
            # Comprobamos si la nueva fecha de vencimiento es válida (renovado)
            if nuevo_doc.fecha_vencimiento and nuevo_doc.fecha_vencimiento > date.today():
                noti = Notificacion.objects.filter(documento=nuevo_doc, estado='Pendiente').first()
                if noti:
                    noti.estado = 'Renovado'
                    noti.fecha_resolucion = timezone.now()
                    noti.save()
            messages.success(request, 'Documento actualizado correctamente.')
        else:
            messages.error(request, 'Revisá los errores del formulario.')
    else:
        form = DocumentoForm(instance=documento)

    return render(request, 'documentos/edit.html', {'form': form, 'id': id})


@require_POST
def delete_document(request, id):
    documento = get_object_or_404(Documento, id=id)
    documento.delete()
    messages.success(request, 'Documento eliminado correctamente.')
    return redirect('documento')


def notificacion(request):
    generar_notificaciones_vencidas()
    notificaciones = Notificacion.objects.filter(estado='Pendiente').order_by('-fecha_envio')
    return render(request, 'notificaciones/index.html', {
        'notificaciones': notificaciones
    })