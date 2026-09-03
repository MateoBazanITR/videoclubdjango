"""
Formularios del videoclub.
Cada formulario valida los datos de entrada de una sección específica:
  - LoginDuenoForm        → autenticación del dueño (clave fija).
  - PeliculaCrearForm     → alta de película (incluye director y cantidades).
  - PeliculaEditarForm    → edición de datos generales de la película.
  - DniForm                → búsqueda de socio por DNI.
  - BusquedaForm           → filtro de búsqueda por título.
  - AlquilerPaso1Form      → primer paso del flujo de alquiler (datos del socio).
"""
from django import forms
from django.core.exceptions import ValidationError

from .models import Pelicula, Socio, Ejemplar

# Clave estática que el dueño debe ingresar para acceder al panel.
CLAVE_DUENO = '2020'


# ─── LOGIN DEL DUEÑO ───
# Solo pide una clave. Se valida contra CLAVE_DUENO.
class LoginDuenoForm(forms.Form):
    clave = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Clave de acceso',
        max_length=50,
        required=True,
    )

    def clean_clave(self):
        clave = self.cleaned_data['clave']
        if clave != CLAVE_DUENO:
            raise ValidationError('Clave incorrecta.')
        return clave


# ─── CREAR PELÍCULA ───
# Recibe todos los datos de la película, del director, cantidad de actores
# y cantidad de ejemplares. Los datos de los actores se procesan aparte
# en la vista (listas paralelas).
class PeliculaCrearForm(forms.Form):
    titulo = forms.CharField(
        max_length=200,
        label='Título',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la película'}),
    )
    nacionalidad = forms.CharField(
        max_length=100,
        label='Nacionalidad',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    productora = forms.CharField(
        max_length=200,
        label='Productora',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    anio = forms.IntegerField(
        label='Año',
        min_value=1888,
        max_value=2100,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    director_nombre = forms.CharField(
        max_length=100,
        label='Director (nombre)',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    director_nacionalidad = forms.CharField(
        max_length=100,
        label='Director (nacionalidad)',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    num_actores = forms.IntegerField(
        label='Cantidad de actores',
        min_value=1,
        max_value=30,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_num_actores'}),
    )
    num_ejemplares = forms.IntegerField(
        label='Cantidad de ejemplares',
        min_value=1,
        max_value=500,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    def clean_director_nombre(self):
        nombre = self.cleaned_data['director_nombre'].strip()
        if not nombre:
            raise ValidationError('El nombre del director es obligatorio.')
        return nombre

    def clean_director_nacionalidad(self):
        nac = self.cleaned_data['director_nacionalidad'].strip()
        if not nac:
            raise ValidationError('La nacionalidad del director es obligatoria.')
        return nac

    def clean(self):
        cleaned = super().clean()
        for campo in ['titulo', 'nacionalidad', 'productora']:
            valor = cleaned.get(campo)
            if valor and not valor.strip():
                self.add_error(campo, 'Este campo no puede estar vacío.')
        return cleaned


# ─── EDITAR PELÍCULA ───
# Similar al de crear pero sin campos de actores ni ejemplares.
class PeliculaEditarForm(forms.Form):
    titulo = forms.CharField(max_length=200, label='Título',
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    nacionalidad = forms.CharField(max_length=100, label='Nacionalidad',
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    productora = forms.CharField(max_length=200, label='Productora',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    anio = forms.IntegerField(label='Año', min_value=1888, max_value=2100,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    director_nombre = forms.CharField(max_length=100, label='Director (nombre)',
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    director_nacionalidad = forms.CharField(max_length=100, label='Director (nacionalidad)',
                                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_director_nombre(self):
        nombre = self.cleaned_data['director_nombre'].strip()
        if not nombre:
            raise ValidationError('El nombre del director es obligatorio.')
        return nombre

    def clean_director_nacionalidad(self):
        nac = self.cleaned_data['director_nacionalidad'].strip()
        if not nac:
            raise ValidationError('La nacionalidad del director es obligatoria.')
        return nac


# ─── CREAR SOCIO ───
# Formulario para que el dueño registre un socio nuevo desde el panel.
class SocioCrearForm(forms.Form):
    dni = forms.CharField(
        max_length=9,
        label='DNI',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej.: 12345678'}),
    )
    nombre = forms.CharField(
        max_length=100,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del socio'}),
    )

    def clean_dni(self):
        dni = self.cleaned_data['dni'].strip()
        if not dni:
            raise ValidationError('Debe ingresar un DNI.')
        if Socio.objects.filter(dni=dni).exists():
            raise ValidationError('Ya existe un socio con ese DNI.')
        return dni

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if not nombre:
            raise ValidationError('Debe ingresar un nombre.')
        return nombre


# ─── FORMULARIO DE BÚSQUEDA POR DNI ───
# Usado tanto por el dueño (devoluciones) como por el cliente (mis alquileres).
class DniForm(forms.Form):
    dni = forms.CharField(
        max_length=9,
        label='DNI',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej.: 12345678'}),
    )

    def clean_dni(self):
        dni = self.cleaned_data['dni'].strip()
        if not dni:
            raise ValidationError('Debe ingresar un DNI.')
        return dni


# ─── FILTRO DE BÚSQUEDA POR TÍTULO ───
# Campo simple "q" para filtrar películas por nombre (case-insensitive).
class BusquedaForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Filtrar por título...'}),
    )


# ─── PASO 1 DEL ALQUILER ───
# Recoge DNI y nombre del socio.
class AlquilerPaso1Form(forms.Form):
    dni = forms.CharField(max_length=9, label='DNI',
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Su DNI'}))
    nombre = forms.CharField(max_length=100, label='Nombre',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Su nombre'}))

    def clean_dni(self):
        dni = self.cleaned_data['dni'].strip()
        if not dni:
            raise ValidationError('Debe ingresar su DNI.')
        return dni

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if not nombre:
            raise ValidationError('Debe ingresar su nombre.')
        return nombre
