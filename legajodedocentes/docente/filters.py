import django_filters
from .models import Docente, NivelDocente
from django.forms.widgets import DateInput


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