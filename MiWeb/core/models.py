"""
Modelos del videoclub.

Las definiciones de las clases viven en `core/entidades.py`.
Este archivo no declara modelos: solo las reexporta.

Django descubre los modelos importando este módulo (`core.models`), que
forma parte de la app `core`. Al importar `entidades`, Django registra
las clases con `app_label = "core"` porque su módulo (`core.entidades`)
pertenece a esa app. Por eso `from core.models import Pelicula` sigue
funcionando igual que antes.

Mover los modelos fuera de este archivo NO cambia la base de datos: los
nombres de tabla (`db_table`) y de columna (`db_column`) viven en cada
clase, dentro de `entidades.py`.
"""

from .entidades import (
    Actor,
    Alquiler,
    Director,
    Ejemplar,
    MovimientoCaja,
    Pelicula,
    PeliculaActor,
    Socio,
)


__all__ = [
    "Director",
    "Actor",
    "Pelicula",
    "PeliculaActor",
    "Ejemplar",
    "Socio",
    "Alquiler",
    "MovimientoCaja",
]