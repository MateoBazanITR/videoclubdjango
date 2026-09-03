"""
Definición de los modelos de la base de datos del videoclub.
Cada clase representa una tabla: directores, actores, películas,
ejemplares físicos, socios del club y alquileres.

Los nombres de tabla (db_table) y columnas (db_column) coinciden
con las tablas existentes en la base de datos MySQL videoclub.
"""
from django.db import models


# ---------- DIRECTOR ----------
class Director(models.Model):
    id_director = models.AutoField(primary_key=True, db_column='id_director')
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50)

    class Meta:
        db_table = 'director'

    def __str__(self):
        return f"{self.nombre} ({self.nacionalidad})"


# ---------- ACTOR ----------
class Actor(models.Model):
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino')]

    id_actor = models.AutoField(primary_key=True, db_column='id_actor')
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    class Meta:
        db_table = 'actor'

    def __str__(self):
        return self.nombre


# ---------- PELICULA ----------
class Pelicula(models.Model):
    id_pelicula = models.AutoField(primary_key=True, db_column='id_pelicula')
    titulo = models.CharField(max_length=150)
    nacionalidad = models.CharField(max_length=50)
    productora = models.CharField(max_length=100)
    anio = models.IntegerField()
    director = models.ForeignKey(
        Director, on_delete=models.CASCADE, related_name='peliculas',
        db_column='id_director'
    )
    actores = models.ManyToManyField(
        Actor, related_name='peliculas',
        through='PeliculaActor',
    )

    class Meta:
        db_table = 'pelicula'

    def __str__(self):
        return self.titulo


# ---------- PELICULA_ACTOR (tabla intermedia M2M) ----------
class PeliculaActor(models.Model):
    pelicula = models.OneToOneField(
        Pelicula, on_delete=models.CASCADE,
        db_column='id_pelicula', primary_key=True
    )
    actor = models.ForeignKey(
        Actor, on_delete=models.CASCADE,
        db_column='id_actor'
    )

    class Meta:
        db_table = 'pelicula_actor'

    def __str__(self):
        return f"{self.pelicula} - {self.actor}"


# ---------- EJEMPLAR ----------
class Ejemplar(models.Model):
    ESTADO_CHOICES = [('Disponible', 'Disponible'), ('Alquilado', 'Alquilado')]

    id_ejemplar = models.AutoField(primary_key=True, db_column='id_ejemplar')
    numero_ejemplar = models.PositiveIntegerField()
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Disponible')
    pelicula = models.ForeignKey(
        Pelicula, on_delete=models.CASCADE, related_name='ejemplares',
        db_column='id_pelicula'
    )

    class Meta:
        db_table = 'ejemplar'
        ordering = ['numero_ejemplar']

    def __str__(self):
        return f"{self.pelicula.titulo} - N° {self.numero_ejemplar}"


# ---------- SOCIO ----------
class Socio(models.Model):
    dni = models.CharField(max_length=15, primary_key=True, db_column='dni')
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    avalador_dni = models.CharField(max_length=15, blank=True, null=True, db_column='avalador_dni')

    class Meta:
        db_table = 'socio'

    def __str__(self):
        return f"{self.nombre} ({self.dni})"


# ---------- ALQUILER ----------
class Alquiler(models.Model):
    id_alquiler = models.AutoField(primary_key=True, db_column='id_alquiler')
    fecha_inicio = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    socio = models.ForeignKey(
        Socio, on_delete=models.CASCADE, related_name='alquileres',
        db_column='dni_socio'
    )
    ejemplar = models.ForeignKey(
        Ejemplar, on_delete=models.CASCADE, related_name='alquileres',
        db_column='id_ejemplar'
    )

    class Meta:
        db_table = 'alquiler'

    def __str__(self):
        return f"{self.socio.dni} - {self.ejemplar}"
