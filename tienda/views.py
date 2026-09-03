from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from . import consultas
from .forms import AlquilerForm, PeliculaForm, SocioForm


def index(request):
    context = {
        'total_peliculas': consultas.total_peliculas(),
        'total_socios': consultas.total_socios(),
        'total_ejemplares': consultas.total_ejemplares(),
        'alquileres_activos': consultas.total_alquileres(True),
        'alquileres_devueltos': consultas.total_alquileres(False),
        'ultimas_peliculas': consultas.ultimas_peliculas(),
        'ultimos_alquileres': consultas.ultimos_alquileres(),
    }
    return render(request, 'tienda/index.html', context)


def pelicula_list(request):
    query = request.GET.get('q', '')
    if query:
        peliculas = consultas.buscar_peliculas(query)
    else:
        peliculas = consultas.todas_las_peliculas()
    return render(
        request,
        'tienda/pelicula_list.html',
        {'peliculas': peliculas, 'query': query},
    )


def pelicula_create(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            consultas.crear_pelicula(
                datos['titulo'],
                datos['nacionalidad'],
                datos['productora'],
                datos['anio'],
                convertir_opcional(datos['director']),
            )
            messages.success(request, 'Película añadida correctamente.')
            return redirect('pelicula_list')
    else:
        form = PeliculaForm()
    return render(
        request,
        'tienda/form.html',
        {'form': form, 'titulo': 'Nueva película', 'cancelar_url': 'pelicula_list'},
    )


def pelicula_update(request, pk):
    pelicula = consultas.pelicula_por_id(pk)
    if pelicula is None:
        raise Http404('No existe esa película.')
    if request.method == 'POST':
        form = PeliculaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            consultas.actualizar_pelicula(
                pk,
                datos['titulo'],
                datos['nacionalidad'],
                datos['productora'],
                datos['anio'],
                convertir_opcional(datos['director']),
            )
            messages.success(request, 'Película actualizada correctamente.')
            return redirect('pelicula_list')
    else:
        form = PeliculaForm(initial={
            'titulo': pelicula['titulo'],
            'nacionalidad': pelicula['nacionalidad'],
            'productora': pelicula['productora'],
            'anio': pelicula['anio'],
            'director': pelicula['director'] if pelicula['director'] != 'Sin director' else '',
        })
    return render(
        request,
        'tienda/form.html',
        {
            'form': form,
            'titulo': 'Editar película',
            'cancelar_url': 'pelicula_list',
        },
    )


def pelicula_delete(request, pk):
    pelicula = consultas.pelicula_por_id(pk)
    if pelicula is None:
        raise Http404('No existe esa película.')
    if consultas.pelicula_tiene_ejemplares(pk):
        messages.error(request, 'No se puede eliminar: la película tiene ejemplares.')
        return redirect('pelicula_list')
    if request.method == 'POST':
        consultas.eliminar_pelicula(pk)
        messages.success(request, 'Película eliminada.')
        return redirect('pelicula_list')
    return render(
        request,
        'tienda/confirm_delete.html',
        {
            'objeto': pelicula['titulo'],
            'titulo': 'Eliminar película',
            'cancelar_url': 'pelicula_list',
        },
    )


def socio_list(request):
    socios = consultas.todos_los_socios()
    return render(request, 'tienda/socio_list.html', {'socios': socios})


def socio_create(request):
    if request.method == 'POST':
        form = SocioForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            consultas.crear_socio(
                datos['dni'],
                datos['nombre'],
                datos['direccion'],
                datos['telefono'],
                datos['avalador_dni'],
            )
            messages.success(request, 'Socio añadido correctamente.')
            return redirect('socio_list')
    else:
        form = SocioForm()
    return render(
        request,
        'tienda/form.html',
        {'form': form, 'titulo': 'Nuevo socio', 'cancelar_url': 'socio_list'},
    )


def socio_update(request, dni):
    socio = consultas.socio_por_id(dni)
    if socio is None:
        raise Http404('No existe ese socio.')
    if request.method == 'POST':
        form = SocioForm(request.POST, dni_actual=dni)
        if form.is_valid():
            datos = form.cleaned_data
            consultas.actualizar_socio(
                dni,
                datos['nombre'],
                datos['direccion'],
                datos['telefono'],
                datos['avalador_dni'],
            )
            messages.success(request, 'Socio actualizado correctamente.')
            return redirect('socio_list')
    else:
        form = SocioForm(initial={
            'dni': socio['dni'],
            'nombre': socio['nombre'],
            'direccion': socio['direccion'],
            'telefono': socio['telefono'],
            'avalador_dni': socio['avalador_dni'],
        }, dni_actual=dni)
    return render(
        request,
        'tienda/form.html',
        {
            'form': form,
            'titulo': 'Editar socio',
            'cancelar_url': 'socio_list',
        },
    )


def socio_delete(request, dni):
    socio = consultas.socio_por_id(dni)
    if socio is None:
        raise Http404('No existe ese socio.')
    if consultas.socio_tiene_alquileres(dni):
        messages.error(request, 'No se puede eliminar: el socio tiene alquileres.')
        return redirect('socio_list')
    if request.method == 'POST':
        consultas.eliminar_socio(dni)
        messages.success(request, 'Socio eliminado.')
        return redirect('socio_list')
    return render(
        request,
        'tienda/confirm_delete.html',
        {
            'objeto': socio['nombre'],
            'titulo': 'Eliminar socio',
            'cancelar_url': 'socio_list',
        },
    )


def alquiler_list(request):
    activos = request.GET.get('activos') == '1'
    if activos:
        alquileres = consultas.alquileres_activos()
    else:
        alquileres = consultas.todos_los_alquileres()
    return render(
        request,
        'tienda/alquiler_list.html',
        {'alquileres': alquileres, 'activos': activos},
    )


def alquiler_create(request):
    if request.method == 'POST':
        form = AlquilerForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            consultas.crear_alquiler(
                datos['socio'],
                int(datos['ejemplar']),
                datos['fecha_inicio'],
            )
            messages.success(request, 'Alquiler registrado correctamente.')
            return redirect('alquiler_list')
    else:
        form = AlquilerForm()
    return render(
        request,
        'tienda/form.html',
        {
            'form': form,
            'titulo': 'Nuevo alquiler',
            'cancelar_url': 'alquiler_list',
        },
    )


def alquiler_devolver(request, pk):
    if not consultas.alquiler_devuelto(pk):
        consultas.devolver_alquiler(pk)
        messages.success(request, 'Alquiler devuelto correctamente.')
    return redirect('alquiler_list')


def convertir_opcional(valor):
    if valor:
        return int(valor)
    return None
