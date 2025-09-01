
from django.urls import path
from docente import views

urlpatterns = [
    # ruta de docentes
    path("",views.index, name="docente"),
    path("view/<int:id>", views.view, name="docente_view"),
    path("edit/<int:id>", views.edit, name="docente_edit"),
    path("create/",views.create, name="docente_create"),
    path("delete/<int:id>/",views.delete, name="docente_delete"),

    # ruta de documentos
    path("documento/",views.documento, name="documento"),
    path("create_document/", views.create_document, name="create_document"),
    path("edit_document/<int:id>", views.edit_document, name="edit_document"),
    path("delete_document/<int:id>/",views.delete_document, name="delete_document"),

    # ruta de notificaciones
    path("notificacion/", views.notificacion, name="notificacion"),

    #ruta de reportes
    path('reportes/documentos/', views.reporte_documentos_form, name='reporte_documentos_form'),
    path('reportes/documentos/export/', views.exportar_documentos, name='exportar_documentos'),


]