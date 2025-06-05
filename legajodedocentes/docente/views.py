from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import DocenteForm, DocumentoForm
from .models import Docente, Documento, Notificacion
from datetime import date
from .utils import generar_notificaciones_vencidas
from .filters import DocenteFilter, DocumentoFilter

# Constantes
DOCENTES_POR_PAGINA = 5
DOCUMENTOS_POR_PAGINA = 6

# ------------------ DOCENTES ------------------

def index(request):
    docente_filter = DocenteFilter(request.GET, queryset=Docente.objects.all().order_by('nombre', 'apellido'))

    paginator = Paginator(docente_filter.qs, DOCENTES_POR_PAGINA)
    page = request.GET.get('page')

    try:
        docentes = paginator.page(page)
    except PageNotAnInteger:
        docentes = paginator.page(1)
    except EmptyPage:
        docentes = paginator.page(paginator.num_pages)

    return render(request, 'docentes/index.html', {
        'docentes': docentes,
        'filter': docente_filter,
    })


def view(request, id):
    docente = get_object_or_404(Docente, id=id)
    return render(request, 'docentes/details.html', {'docente': docente})


def create(request):
    form = DocenteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Docente agregado correctamente.')
            return redirect('docente')
        messages.error(request, 'Revisá los errores del formulario.')
    return render(request, 'docentes/create.html', {'form': form})


def edit(request, id):
    docente = get_object_or_404(Docente, id=id)
    form = DocenteForm(request.POST or None, instance=docente)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Docente actualizado correctamente.')
        else:
            messages.error(request, 'Revisá los errores del formulario.')
    return render(request, 'docentes/edit.html', {'form': form, 'id': id})


@require_POST
def delete(request, id):
    docente = get_object_or_404(Docente, id=id)
    docente.delete()
    messages.success(request, 'Docente eliminado correctamente.')
    return redirect('docente')


# ------------------ DOCUMENTOS ------------------

def documento(request):
    documento_filter = DocumentoFilter(
        request.GET,
        queryset=Documento.objects.all().order_by('-fecha_emision')
    )
    # query = request.GET.get('search', '')
    # documentos_list = Documento.objects.filter(
    #     Q(nombre__icontains=query) |
    #     Q(docente__nombre__icontains=query) |
    #     Q(docente__apellido__icontains=query) |
    #     Q(docente__ci__icontains=query) |
    #     Q(tipo_documento__nombre__icontains=query)
    # ).order_by('-fecha_emision')

    paginator = Paginator(documento_filter.qs, DOCUMENTOS_POR_PAGINA)
    page = request.GET.get('page')

    try:
        documentos = paginator.page(page)
    except PageNotAnInteger:
        documentos = paginator.page(1)
    except EmptyPage:
        documentos = paginator.page(paginator.num_pages)

    return render(request, 'documentos/index.html', {
        'documentos': documentos,
        # 'query': query,
        'filter': documento_filter,
    })


def create_document(request):
    form = DocumentoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento agregado correctamente.')
            return redirect('documento')
        messages.error(request, 'Revisá los errores del formulario.')
    return render(request, 'documentos/create.html', {'form': form})


def edit_document(request, id):
    documento = get_object_or_404(Documento, id=id)
    form = DocumentoForm(request.POST or None, request.FILES or None, instance=documento)

    if request.method == 'POST':
        if form.is_valid():
            nuevo_doc = form.save()
            if nuevo_doc.fecha_vencimiento and nuevo_doc.fecha_vencimiento > date.today():
                noti = Notificacion.objects.filter(documento=nuevo_doc, estado='Pendiente').first()
                if noti:
                    noti.estado = 'Renovado'
                    noti.fecha_resolucion = timezone.now()
                    noti.save()
            messages.success(request, 'Documento actualizado correctamente.')
        else:
            messages.error(request, 'Revisá los errores del formulario.')

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
