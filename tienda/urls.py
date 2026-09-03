from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('peliculas/', views.pelicula_list, name='pelicula_list'),
    path('peliculas/nueva/', views.pelicula_create, name='pelicula_create'),
    path('peliculas/<int:pk>/editar/', views.pelicula_update, name='pelicula_update'),
    path('peliculas/<int:pk>/eliminar/', views.pelicula_delete, name='pelicula_delete'),
    path('socios/', views.socio_list, name='socio_list'),
    path('socios/nuevo/', views.socio_create, name='socio_create'),
    path('socios/<str:dni>/editar/', views.socio_update, name='socio_update'),
    path('socios/<str:dni>/eliminar/', views.socio_delete, name='socio_delete'),
    path('alquileres/', views.alquiler_list, name='alquiler_list'),
    path('alquileres/nuevo/', views.alquiler_create, name='alquiler_create'),
    path('alquileres/<int:pk>/devolver/', views.alquiler_devolver, name='alquiler_devolver'),
]
