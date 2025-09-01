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

from django.contrib.auth.decorators import login_required, permission_required

# Constantes
DOCENTES_POR_PAGINA = 5
DOCUMENTOS_POR_PAGINA = 6


# ------------------ DOCENTES ------------------
@login_required
def index(request):
    search_query = request.GET.get('search', '')

    # Base queryset
    docentes = Docente.objects.all().order_by('apellido', 'nombre')

    # Aplicar búsqueda global si existe
    if search_query:
        docentes = docentes.filter(
            Q(nombre__icontains=search_query) |
            Q(apellido__icontains=search_query) |
            Q(ci__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Aplicar filtros
    docente_filter = DocenteFilter(request.GET, queryset=docentes)
    docentes_filtrados = docente_filter.qs

    # Paginación
    paginator = Paginator(docentes_filtrados, 10)  # Ajusta el número por página
    page = request.GET.get('page')

    try:
        docentes_paginados = paginator.page(page)
    except PageNotAnInteger:
        docentes_paginados = paginator.page(1)
    except EmptyPage:
        docentes_paginados = paginator.page(paginator.num_pages)

    return render(request, 'docentes/index.html', {
        'docentes': docentes_paginados,
        'filter': docente_filter,
        'search_query': search_query,
    })


@login_required
def view(request, id):
    docente = get_object_or_404(Docente, id=id)
    return render(request, 'docentes/details.html', {'docente': docente})


@login_required
@permission_required("docente.add_documento", raise_exception=True)
def create(request):
    form = DocenteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Docente agregado correctamente.')
            return redirect('docente')
        messages.error(request, 'Revisá los errores del formulario.')
    return render(request, 'docentes/create.html', {'form': form})


@login_required
@permission_required("docente.change_documento", raise_exception=True)
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


@login_required
@permission_required("docente.delete_documento", raise_exception=True)
@require_POST
def delete(request, id):
    docente = get_object_or_404(Docente, id=id)
    docente.delete()
    messages.success(request, 'Docente eliminado correctamente.')
    return redirect('docente')


# ------------------ DOCUMENTOS ------------------
@login_required
def documento(request):
    # Obtener parámetros
    search_query = request.GET.get('search', '')

    # Base queryset
    documentos = Documento.objects.select_related(
        'docente', 'tipo_documento'
    ).order_by('-fecha_emision')

    # Aplicar búsqueda global si existe
    if search_query:
        documentos = documentos.filter(
            Q(nombre__icontains=search_query) |
            Q(docente__nombre__icontains=search_query) |
            Q(docente__apellido__icontains=search_query) |
            Q(docente__ci__icontains=search_query) |
            Q(tipo_documento__nombre__icontains=search_query)
        )

    # Aplicar filtros
    documento_filter = DocumentoFilter(request.GET, queryset=documentos)
    documentos_filtrados = documento_filter.qs

    # Paginación
    paginator = Paginator(documentos_filtrados, DOCUMENTOS_POR_PAGINA)
    page = request.GET.get('page')

    try:
        documentos_paginados = paginator.page(page)
    except PageNotAnInteger:
        documentos_paginados = paginator.page(1)
    except EmptyPage:
        documentos_paginados = paginator.page(paginator.num_pages)

    return render(request, 'documentos/index.html', {
        'documentos': documentos_paginados,
        'filter': documento_filter,
        'search_query': search_query,
    })


@login_required
@permission_required("docente.add_documento", raise_exception=True)

def create_document(request):
    form = DocumentoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento agregado correctamente.')
            return redirect('documento')
        messages.error(request, 'Revisá los errores del formulario.')
    return render(request, 'documentos/create.html', {'form': form})


@login_required
@permission_required("docente.change_documento", raise_exception=True)
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


@login_required
@permission_required("docente.delete_documento", raise_exception=True)
@require_POST
def delete_document(request, id):
    documento = get_object_or_404(Documento, id=id)
    documento.delete()
    messages.success(request, 'Documento eliminado correctamente.')
    return redirect('documento')

@login_required
def notificacion(request):
    generar_notificaciones_vencidas()
    notificaciones = Notificacion.objects.filter(estado='Pendiente').order_by('-fecha_envio')
    return render(request, 'notificaciones/index.html', {
        'notificaciones': notificaciones
    })
