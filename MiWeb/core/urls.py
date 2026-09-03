"""
URLs de la aplicación "core".
Se organizan en dos grupos:
  - /dueno/...  → secciones administrativas (protegidas por sesión).
  - /cliente/... → áreas públicas para los socios.
"""
from django.urls import path

from . import views

urlpatterns = [
    # Página de inicio
    path('', views.index, name='index'),

    # ─── Sección del dueño ───
    path('dueno/login/', views.login_dueno, name='login_dueno'),       # Login
    path('dueno/logout/', views.logout_dueno, name='logout_dueno'),    # Logout
    path('dueno/panel/', views.panel_dueno, name='panel_dueno'),       # Panel principal

    # CRUD de películas
    path('dueno/peliculas/', views.dueno_peliculas, name='dueno_peliculas'),
    path('dueno/peliculas/nueva/', views.pelicula_crear, name='pelicula_crear'),
    path('dueno/peliculas/<int:pk>/editar/', views.pelicula_editar, name='pelicula_editar'),
    path('dueno/peliculas/<int:pk>/eliminar/', views.pelicula_eliminar, name='pelicula_eliminar'),

    # Gestión de socios
    path('dueno/socios/', views.dueno_socios, name='dueno_socios'),
    path('dueno/socios/nueva/', views.socio_crear, name='socio_crear'),
    path('dueno/socios/<str:dni>/eliminar/', views.socio_eliminar, name='socio_eliminar'),

    # Devolución de ejemplares
    path('dueno/devolver/', views.devolver, name='devolver'),

    # ─── Sección del cliente ───
    path('cliente/peliculas/', views.cliente_peliculas, name='cliente_peliculas'),  # Catálogo

    # Flujo de alquiler (3 pasos + confirmación)
    path('cliente/alquilar/', views.alquilar_paso1, name='alquilar_paso1'),                 # Paso 1: socio
    path('cliente/alquilar/paso2/', views.alquilar_paso2, name='alquilar_paso2'),           # Paso 2: película
    path('cliente/alquilar/paso3/<int:pelicula_id>/', views.alquilar_paso3, name='alquilar_paso3'),  # Paso 3: ejemplar
    path('cliente/alquilar/confirmar/<int:ejemplar_id>/', views.alquilar_confirmar, name='alquilar_confirmar'),  # Confirmar

    # Consulta de alquileres activos del socio
    path('cliente/mis-alquileres/', views.mis_alquileres, name='mis_alquileres'),
]
