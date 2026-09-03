"""
Vistas del videoclub.
Se dividen en dos grandes bloques:
  - DUEÑO: administración de películas, socios y devoluciones (requiere login).
  - CLIENTE: catálogo, flujo de alquiler en 3 pasos y consulta de alquileres.
"""
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from .import forms

'''
from .forms import (
    LoginDuenoForm,
    PeliculaCrearForm,
    PeliculaEditarForm,
    SocioCrearForm,
    DniForm,
    BusquedaForm,
    AlquilerPaso1Form,
)
'''
from .models import Director, Actor, Pelicula, PeliculaActor, Ejemplar, Socio, Alquiler

# Límite de alquileres simultáneos por socio.
MAX_ALQUILERES_ACTIVOS = 4


# ---------------------------------------------------------------- UTILIDAD
# Decorador que protege las vistas del dueño: si no hay sesión de dueño
# redirige al login.
def requerir_dueno(vista):
    def envoltura(request, *args, **kwargs):
        if not request.session.get('es_dueno'):
            messages.error(request, 'Debe iniciar sesión como dueño para acceder.')
            return redirect('login_dueno')
        return vista(request, *args, **kwargs)
    return envoltura


# Página de inicio (accesible para todos).
def index(request):
    return render(request, 'core/index.html')


# ---------------------------------------------------------------- DUEÑO

# Login del dueño: valida la clave y guarda un flag en la sesión.
def login_dueno(request):
    if request.method == 'POST':
        form = LoginDuenoForm(request.POST)
        if form.is_valid():
            request.session['es_dueno'] = True
            messages.success(request, 'Bienvenido, dueño del videoclub.')
            return redirect('panel_dueno')
    else:
        form = LoginDuenoForm()
    return render(request, 'core/dueno_login.html', {'form': form})


# Cierra la sesión del dueño y vuelve al inicio.
def logout_dueno(request):
    request.session.pop('es_dueno', None)
    messages.success(request, 'Sesión de dueño cerrada.')
    return redirect('index')


# Panel principal del dueño (acceso rápido a las distintas secciones).
@requerir_dueno
def panel_dueno(request):
    return render(request, 'core/dueno_panel.html')


# ---------------------------------------------------------------- DUEÑO – PELÍCULAS

# Lista todas las películas con cantidad total de ejemplares y disponibles.
# Permite filtrar por título con el parámetro GET "q".
@requerir_dueno
def dueno_peliculas(request):
    form = BusquedaForm(request.GET)
    peliculas = Pelicula.objects.select_related('director').annotate(
        num_ejemplares=Count('ejemplares'),
        disponibles=Count('ejemplares', filter=Q(ejemplares__estado='Disponible')),
    ).order_by('titulo')
    q = request.GET.get('q', '').strip()
    if q:
        peliculas = peliculas.filter(titulo__icontains=q)
    return render(request, 'core/dueno_peliculas.html', {
        'peliculas': peliculas,
        'form': form,
        'q': q,
    })


# Alta de una película nueva junto con su director, actores y ejemplares.
# Los actores se reciben como listas paralelas (nombre[], nacionalidad[], sexo[]).
# Si el director ya existe se reutiliza; si no, se crea automáticamente.
@requerir_dueno
def pelicula_crear(request):
    if request.method == 'POST':
        form = PeliculaCrearForm(request.POST)
        nombres = request.POST.getlist('actor_nombre')
        nacionalidades = request.POST.getlist('actor_nacionalidad')
        sexos = request.POST.getlist('actor_sexo')

        if form.is_valid():
            datos = form.cleaned_data
            num_actores = datos['num_actores']

            # Validación manual de los datos de actores
            error_actores = None
            if len(nombres) != num_actores:
                error_actores = f'Debe completar los datos de los {num_actores} actores.'
            elif not all(n.strip() for n in nombres):
                error_actores = 'Todos los actores deben tener un nombre.'
            elif any(not n.strip() for n in nacionalidades):
                error_actores = 'Todos los actores deben tener nacionalidad.'
            elif any(not s.strip() for s in sexos):
                error_actores = 'Todos los actores deben tener sexo.'

            if error_actores:
                messages.error(request, error_actores)
                return render(request, 'core/pelicula_form.html', {
                    'form': form,
                    'nombres': nombres,
                    'nacionalidades': nacionalidades,
                    'sexos': sexos,
                })

            # Busca el director por nombre; si no existe lo crea
            director = Director.objects.filter(nombre__iexact=datos['director_nombre']).first()
            if not director:
                director = Director.objects.create(
                    nombre=datos['director_nombre'],
                    nacionalidad=datos['director_nacionalidad'],
                )

            # Crea la película
            pelicula = Pelicula.objects.create(
                titulo=datos['titulo'].strip(),
                nacionalidad=datos['nacionalidad'].strip(),
                productora=datos['productora'].strip(),
                anio=datos['anio'],
                director=director,
            )

            # Crea cada actor y lo asocia a la película
            for nombre, nacionalidad, sexo in zip(nombres, nacionalidades, sexos):
                actor = Actor.objects.create(
                    nombre=nombre.strip(),
                    nacionalidad=nacionalidad.strip(),
                    sexo=sexo.strip(),
                )
                PeliculaActor.objects.create(pelicula=pelicula, actor=actor)

            # Crea los ejemplares físicos (todas disponibles)
            for i in range(datos['num_ejemplares']):
                Ejemplar.objects.create(
                    numero_ejemplar=i + 1,
                    estado='Disponible',
                    pelicula=pelicula,
                )

            messages.success(request, f'Película "{pelicula.titulo}" registrada correctamente.')
            return redirect('dueno_peliculas')
    else:
        form = PeliculaCrearForm()
        nombres = nacionalidades = sexos = []

    return render(request, 'core/pelicula_form.html', {
        'form': form,
        'nombres': nombres,
        'nacionalidades': nacionalidades,
        'sexos': sexos,
    })


# Edita los datos generales de una película (título, año, director, etc.).
# No permite modificar los ejemplares ni los actores desde acá.
@requerir_dueno
def pelicula_editar(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)

    if request.method == 'POST':
        form = PeliculaEditarForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            director = Director.objects.filter(nombre__iexact=datos['director_nombre']).first()
            if not director:
                director = Director.objects.create(
                    nombre=datos['director_nombre'],
                    nacionalidad=datos['director_nacionalidad'],
                )
            pelicula.titulo = datos['titulo'].strip()
            pelicula.nacionalidad = datos['nacionalidad'].strip()
            pelicula.productora = datos['productora'].strip()
            pelicula.anio = datos['anio']
            pelicula.director = director
            pelicula.save()
            messages.success(request, f'Película "{pelicula.titulo}" modificada correctamente.')
            return redirect('dueno_peliculas')
    else:
        # Precarga el formulario con los valores actuales de la película
        form = PeliculaEditarForm(initial={
            'titulo': pelicula.titulo,
            'nacionalidad': pelicula.nacionalidad,
            'productora': pelicula.productora,
            'anio': pelicula.anio,
            'director_nombre': pelicula.director.nombre,
            'director_nacionalidad': pelicula.director.nacionalidad,
        })

    return render(request, 'core/pelicula_editar.html', {'form': form, 'pelicula': pelicula})


# Elimina una película y todos sus datos asociados (cascada).
@requerir_dueno
def pelicula_eliminar(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)

    if request.method == 'POST':
        titulo = pelicula.titulo
        pelicula.delete()
        messages.success(request, f'La película "{titulo}" y todos sus datos fueron eliminados.')
        return redirect('dueno_peliculas')

    return render(request, 'core/pelicula_confirmar.html', {'pelicula': pelicula})


# ---------------------------------------------------------------- DUEÑO – SOCIOS

# Lista todos los socios con sus alquileres activos (sin devolver).
@requerir_dueno
def dueno_socios(request):
    socios = Socio.objects.prefetch_related('alquileres__ejemplar__pelicula').order_by('dni')
    lista = []
    for socio in socios:
        activos = socio.alquileres.filter(fecha_devolucion__isnull=True).select_related('ejemplar__pelicula')
        lista.append((socio, activos))
    return render(request, 'core/dueno_socios.html', {'socios': lista})


# Alta de un socio nuevo desde el panel del dueño.
@requerir_dueno
def socio_crear(request):
    if request.method == 'POST':
        form = SocioCrearForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            socio = Socio.objects.create(
                dni=datos['dni'],
                nombre=datos['nombre'],
            )
            messages.success(request, f'Socio "{socio.nombre}" registrado correctamente.')
            return redirect('dueno_socios')
    else:
        form = SocioCrearForm()
    return render(request, 'core/socio_form.html', {'form': form})


# Elimina un socio.
@requerir_dueno
def socio_eliminar(request, dni):
    socio = get_object_or_404(Socio, pk=dni)

    if request.method == 'POST':
        nombre = socio.nombre
        socio.delete()
        messages.success(request, f'El socio {nombre} fue eliminado (sus alquileres se borraron).')
        return redirect('dueno_socios')

    return render(request, 'core/socio_confirmar.html', {'socio': socio})


# ---------------------------------------------------------------- DUEÑO – DEVOLUCIONES

# Flujo de devolución en dos pasos:
#   1) Se ingresa el DNI del socio → se listan sus alquileres activos.
#   2) Se elige un alquiler → se marca como devuelto y el ejemplar vuelve a "Disponible".
@requerir_dueno
def devolver(request):
    socio = None
    activos = []
    dni_form = DniForm()

    if request.method == 'POST':
        if 'alquiler_id' in request.POST:
            # Paso 2: confirma la devolución de un alquiler específico
            alquiler = get_object_or_404(Alquiler, pk=request.POST['alquiler_id'])
            if alquiler.fecha_devolucion is None:
                alquiler.fecha_devolucion = timezone.localdate()
                alquiler.save()
                ejemplar = alquiler.ejemplar
                ejemplar.estado = 'Disponible'
                ejemplar.save()
                messages.success(request, f'Alquiler devuelto: {ejemplar} ({alquiler.socio.nombre}).')
            else:
                messages.info(request, 'Ese alquiler ya estaba devuelto.')
            socio = alquiler.socio
            dni_form = DniForm(initial={'dni': socio.dni})
        else:
            # Paso 1: busca el socio por DNI
            dni_form = DniForm(request.POST)
            if dni_form.is_valid():
                dni = dni_form.cleaned_data['dni']
                socio = Socio.objects.filter(dni=dni).first()
                if not socio:
                    messages.error(request, f'No existe un socio con DNI {dni}.')
                else:
                    messages.success(request, f'Socio encontrado: {socio.nombre}.')

    if socio:
        activos = (socio.alquileres
                   .filter(fecha_devolucion__isnull=True)
                   .select_related('ejemplar__pelicula'))

    return render(request, 'core/devolver.html', {
        'dni_form': dni_form,
        'socio': socio,
        'activos': activos,
    })


# ---------------------------------------------------------------- CLIENTE

# Catálogo público: solo muestra películas que tengan al menos un ejemplar
# disponible. Soporta búsqueda por título.
def cliente_peliculas(request):
    peliculas = Pelicula.objects.annotate(
        disponibles=Count('ejemplares', filter=Q(ejemplares__estado='Disponible')),
    ).filter(disponibles__gt=0).order_by('titulo')

    q = request.GET.get('q', '').strip()
    if q:
        peliculas = peliculas.filter(titulo__icontains=q)

    return render(request, 'core/cliente_peliculas.html', {
        'peliculas': peliculas,
        'q': q,
    })


# ---------------------------------------------------------------- ALQUILER – PASO 1
# El socio ingresa su DNI y nombre. Si ya está registrado se valida que no
# tenga 4 alquileres activos. Si es nuevo se registra automáticamente.
def alquilar_paso1(request):
    if request.method == 'POST':
        form = AlquilerPaso1Form(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            nombre = form.cleaned_data['nombre']

            socio = Socio.objects.filter(dni=dni).first()

            if socio:
                # Socio ya registrado: verifica el límite de alquileres
                if socio.alquileres.filter(fecha_devolucion__isnull=True).count() >= MAX_ALQUILERES_ACTIVOS:
                    messages.error(request, 'Este socio ya tiene 4 alquileres activos.')
                else:
                    request.session['alquiler_dni'] = socio.dni
                    request.session['alquiler_nombre'] = socio.nombre
                    return redirect('alquilar_paso2')
            else:
                # Socio nuevo: se registra automáticamente
                socio = Socio.objects.create(dni=dni, nombre=nombre)
                messages.success(request, f'¡Socio {nombre} registrado correctamente!')
                request.session['alquiler_dni'] = socio.dni
                request.session['alquiler_nombre'] = socio.nombre
                return redirect('alquilar_paso2')
        # se re-renderiza con errores
        return render(request, 'core/alquilar_paso1.html', {'form': form})

    form = AlquilerPaso1Form()
    return render(request, 'core/alquilar_paso1.html', {'form': form})


# ---------------------------------------------------------------- ALQUILER – PASO 2
# Muestra las películas disponibles para que el socio elija cuál quiere alquilar.
def alquilar_paso2(request):
    dni = request.session.get('alquiler_dni')
    if not dni:
        messages.warning(request, 'Debe iniciar el alquiler desde el principio.')
        return redirect('alquilar_paso1')
    socio = get_object_or_404(Socio, pk=dni)

    q = request.GET.get('q', '').strip()
    peliculas = Pelicula.objects.annotate(
        disponibles=Count('ejemplares', filter=Q(ejemplares__estado='Disponible')),
    ).filter(disponibles__gt=0).order_by('titulo')
    if q:
        peliculas = peliculas.filter(titulo__icontains=q)

    return render(request, 'core/alquilar_paso2.html', {
        'socio': socio,
        'peliculas': peliculas,
        'q': q,
    })


# ---------------------------------------------------------------- ALQUILER – PASO 3
# Muestra los ejemplares disponibles de la película elegida.
def alquilar_paso3(request, pelicula_id):
    dni = request.session.get('alquiler_dni')
    if not dni:
        messages.warning(request, 'Debe iniciar el alquiler desde el principio.')
        return redirect('alquilar_paso1')
    socio = get_object_or_404(Socio, pk=dni)

    if socio.alquileres.filter(fecha_devolucion__isnull=True).count() >= MAX_ALQUILERES_ACTIVOS:
        messages.error(request, 'Este socio ya tiene 4 alquileres activos.')
        return redirect('mis_alquileres')

    pelicula = get_object_or_404(Pelicula, pk=pelicula_id)
    ejemplares = pelicula.ejemplares.filter(estado='Disponible')
    if not ejemplares.exists():
        messages.error(request, 'Esta película ya no tiene ejemplares disponibles.')
        return redirect('alquilar_paso2')

    return render(request, 'core/alquilar_paso3.html', {
        'socio': socio,
        'pelicula': pelicula,
        'ejemplares': ejemplares,
    })


# Confirma el alquiler: crea el registro de Alquiler, marca el ejemplar
# como "Alquilado" y limpia la sesión del flujo de alquiler.
def alquilar_confirmar(request, ejemplar_id):
    if request.method != 'POST':
        return redirect('alquilar_paso1')

    dni = request.session.get('alquiler_dni')
    if not dni:
        messages.warning(request, 'Debe iniciar el alquiler desde el principio.')
        return redirect('alquilar_paso1')
    socio = get_object_or_404(Socio, pk=dni)

    if socio.alquileres.filter(fecha_devolucion__isnull=True).count() >= MAX_ALQUILERES_ACTIVOS:
        messages.error(request, 'Este socio ya tiene 4 alquileres activos.')
        request.session.pop('alquiler_dni', None)
        return redirect('mis_alquileres')

    ejemplar = get_object_or_404(Ejemplar, pk=ejemplar_id)
    if ejemplar.estado != 'Disponible':
        messages.error(request, 'Ese ejemplar ya no está disponible.')
        return redirect('alquilar_paso2')

    Alquiler.objects.create(
        socio=socio,
        ejemplar=ejemplar,
        fecha_inicio=timezone.localdate(),
    )
    ejemplar.estado = 'Alquilado'
    ejemplar.save()

    messages.success(request, f'Alquiler confirmado: {ejemplar} desde hoy.')
    request.session.pop('alquiler_dni', None)
    request.session.pop('alquiler_nombre', None)
    return redirect('mis_alquileres')


# Consulta de alquileres activos: el socio ingresa su DNI y ve qué tiene alquilado.
def mis_alquileres(request):
    socio = None
    activos = []
    dni_form = DniForm()

    if request.method == 'POST':
        dni_form = DniForm(request.POST)
        if dni_form.is_valid():
            dni = dni_form.cleaned_data['dni']
            socio = Socio.objects.filter(dni=dni).first()
            if not socio:
                messages.error(request, f'No existe un socio con DNI {dni}.')
            else:
                activos = (socio.alquileres
                           .filter(fecha_devolucion__isnull=True)
                           .select_related('ejemplar__pelicula'))

    return render(request, 'core/mis_alquileres.html', {
        'dni_form': dni_form,
        'socio': socio,
        'activos': activos,
    })
