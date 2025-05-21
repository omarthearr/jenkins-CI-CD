from django import forms
from .models import Materia, UnidadAcademica, ProgramaAcademico


class FormFiltrosProgramaAcademico(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Programa'})
    )
    unidad_academica = forms.CharField(
        label='Unidad académica',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Unidad'})
    )
    abreviacion = forms.CharField(
        label='Abreviación',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Abreviación'})
    )


class FormProgramaAcademimco(forms.ModelForm):
    class Meta:
        model = ProgramaAcademico
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingeniería de Software'
                }
            ),
            'abreviacion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'IS'
                }
            ),
            'unidad_academica': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }


class FormUnidadAcademica(forms.ModelForm):
    class Meta:
        model = UnidadAcademica
        # fields = ['nombre','abreviacion']
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Unidad Académica de Ingeniería Eléctrica'
                }
            ),
            'abreviacion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'UIAE'
                }
            ),
        }


class FormMateria(forms.ModelForm):
    class Meta:
        model = Materia
        # fields = ['clave', 'nombre']
        # fields = '__all__'
        exclude = ['descripcion']
