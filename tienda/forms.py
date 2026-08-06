from django import forms

from . import consultas


class PeliculaForm(forms.Form):
    titulo = forms.CharField(max_length=150, label='Título')
    nacionalidad = forms.CharField(
        max_length=50, required=False, label='Nacionalidad'
    )
    productora = forms.CharField(
        max_length=100, required=False, label='Productora'
    )
    anio = forms.IntegerField(
        label='Año', required=False, min_value=1888, max_value=2100
    )
    director = forms.ChoiceField(label='Director', choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        opciones = [
            (d['pk'], d['nombre']) for d in consultas.todos_los_directores()
        ]
        self.fields['director'].choices = [('', 'Sin director')] + opciones


class SocioForm(forms.Form):
    dni = forms.CharField(max_length=15, label='DNI')
    nombre = forms.CharField(max_length=100, label='Nombre')
    direccion = forms.CharField(max_length=200, required=False, label='Dirección')
    telefono = forms.CharField(max_length=30, required=False, label='Teléfono')
    avalador_dni = forms.CharField(
        max_length=15, required=False, label='DNI del avalador'
    )

    def __init__(self, *args, dni_actual=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.dni_actual = dni_actual

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if dni != self.dni_actual and consultas.existe_socio(dni):
            raise forms.ValidationError('Ya existe un socio con este DNI.')
        return dni

    def clean_avalador_dni(self):
        avalador = self.cleaned_data.get('avalador_dni')
        if not avalador:
            return None
        if not consultas.existe_socio(avalador):
            raise forms.ValidationError('No existe ningún socio con ese DNI.')
        return avalador


class AlquilerForm(forms.Form):
    socio = forms.ChoiceField(label='Socio', choices=[])
    ejemplar = forms.ChoiceField(label='Ejemplar', choices=[])
    fecha_inicio = forms.DateField(
        label='Fecha de inicio',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        opciones_socios = [
            (s['dni'], s['nombre'] + ' (' + s['dni'] + ')')
            for s in consultas.todos_los_socios()
        ]
        self.fields['socio'].choices = opciones_socios
        opciones_ejemplares = [
            (
                e['pk'],
                e['pelicula'] + ' · Nº ' + str(e['numero']),
            )
            for e in consultas.todos_los_ejemplares()
        ]
        self.fields['ejemplar'].choices = opciones_ejemplares
