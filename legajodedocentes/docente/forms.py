from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, EmailInput, DateInput, Select
from django.forms.widgets import ClearableFileInput

from .models import Docente, Documento


class DocenteForm(ModelForm):
    class Meta:
        model = Docente
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'apellido': TextInput(attrs={'class': 'form-control'}),
            'ci': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'telefono': TextInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': DateInput(format='%Y-%m-%d', attrs={
                'type': 'date',
                'class': 'form-control',
                'max': date.today().isoformat(),
            }),
            'nivel': Select(attrs={'class': 'form-select'}),
        }

    def clean_fecha_ingreso(self):
        fecha_ingreso = self.cleaned_data.get('fecha_ingreso')
        if fecha_ingreso and fecha_ingreso > date.today():
            raise forms.ValidationError('La fecha de ingreso no puede ser posterior a hoy.')
        return fecha_ingreso


class DocumentoForm(ModelForm):
    class Meta:
        model = Documento
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'fecha_emision': DateInput(format='%Y-%m-%d', attrs={
                'type': 'date',
                'class': 'form-control',
                'max': date.today().isoformat(),
            }),
            'fecha_vencimiento': DateInput(format='%Y-%m-%d', attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'archivo': ClearableFileInput(attrs={'class': 'form-control'}),
            'docente': Select(attrs={'class': 'form-select'}),
            'tipo_documento': Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_emision = cleaned_data.get('fecha_emision')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')

        if fecha_emision:
            if fecha_emision > date.today():
                self.add_error('fecha_emision', 'La fecha de emisión no puede ser posterior a hoy.')

        if fecha_emision and fecha_vencimiento:
            if fecha_vencimiento < fecha_emision:
                self.add_error('fecha_vencimiento', 'La fecha de vencimiento no puede ser anterior a la de emisión.')

        return cleaned_data
