import django_filters
from .models import Docente, NivelDocente, Documento, TipoDocumento
from django.forms.widgets import DateInput
from django import forms

# class DocumentoFilter(django_filters.FilterSet):
#     nombre = django_filters.CharFilter(lookup_expr='icontains', label='Nombre del documento')
#     fecha_emision = django_filters.DateFromToRangeFilter(
#         label='Fecha de emisión (rango)',
#         widget=django_filters.widgets.RangeWidget(attrs={'type': 'date', 'class': 'form-control'})
#     )
#     fecha_vencimiento = django_filters.DateFromToRangeFilter(
#         label='Fecha de vencimiento (rango)',
#         widget=django_filters.widgets.RangeWidget(attrs={'type': 'date', 'class': 'form-control'})
#     )
#     tipo_documento = django_filters.ModelChoiceFilter(
#         queryset=TipoDocumento.objects.all(),
#         label='Tipo de documento',
#         empty_label='Todos los tipos'
#     )
#     docente = django_filters.ModelChoiceFilter(
#         queryset=Docente.objects.all(),
#         label='Docente',
#         empty_label='Todos los docentes'
#     )
#
#     class Meta:
#         model = Documento
#         fields = ['nombre', 'fecha_emision', 'fecha_vencimiento', 'tipo_documento', 'docente']

class DocumentoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del documento'
        })
    )

    tipo_documento = django_filters.ModelChoiceFilter(
        queryset=TipoDocumento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    docente = django_filters.ModelChoiceFilter(
        queryset=Docente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Docente"
    )

    fecha_emision = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    fecha_vencimiento = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = Documento
        fields = ['nombre', 'tipo_documento', 'docente', 'fecha_emision', 'fecha_vencimiento']

class DocenteFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains', label='Nombre contiene')
    apellido = django_filters.CharFilter(lookup_expr='icontains', label='Apellido contiene')
    ci = django_filters.CharFilter(lookup_expr='icontains', label='CI contiene')
    email = django_filters.CharFilter(lookup_expr='icontains', label='Email contiene')
    telefono = django_filters.CharFilter(lookup_expr='icontains', label='Teléfono contiene')

    fecha_ingreso_min = django_filters.DateFilter(
        field_name='fecha_ingreso',
        lookup_expr='gte',
        label='Fecha ingreso desde',
        widget=DateInput(attrs={'type': 'date'})
    )
    fecha_ingreso_max = django_filters.DateFilter(
        field_name='fecha_ingreso',
        lookup_expr='lte',
        label='Fecha ingreso hasta',
        widget=DateInput(attrs={'type': 'date'})
    )

    nivel = django_filters.ModelChoiceFilter(
        queryset=NivelDocente.objects.all(),
        label='Nivel docente',
        empty_label="Todos los niveles"
    )

    class Meta:
        model = Docente
        fields = []


