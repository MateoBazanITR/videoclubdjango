from django.db import connection


def todos_los_directores():
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id_director, nombre "
        "FROM director ORDER BY nombre"
    )
    directores = []
    for fila in cursor.fetchall():
        directores.append({'pk': fila[0], 'nombre': fila[1]})
    return directores


def todas_las_peliculas():
    cursor = connection.cursor()
    cursor.execute(
        "SELECT p.id_pelicula, p.titulo, p.nacionalidad, p.productora, "
        "p.anio, d.nombre "
        "FROM pelicula p "
        "LEFT JOIN director d ON p.id_director = d.id_director "
        "ORDER BY p.titulo"
    )
    peliculas = []
    for fila in cursor.fetchall():
        peliculas.append(convertir_pelicula(fila))
    return peliculas


def buscar_peliculas(titulo):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT p.id_pelicula, p.titulo, p.nacionalidad, p.productora, "
        "p.anio, d.nombre "
        "FROM pelicula p "
        "LEFT JOIN director d ON p.id_director = d.id_director "
        "WHERE p.titulo LIKE %s "
        "ORDER BY p.titulo",
        ['%' + titulo + '%'],
    )
    peliculas = []
    for fila in cursor.fetchall():
        peliculas.append(convertir_pelicula(fila))
    return peliculas


def pelicula_por_id(pelicula_id):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT p.id_pelicula, p.titulo, p.nacionalidad, p.productora, "
        "p.anio, d.nombre "
        "FROM pelicula p "
        "LEFT JOIN director d ON p.id_director = d.id_director "
        "WHERE p.id_pelicula = %s",
        [pelicula_id],
    )
    fila = cursor.fetchone()
    if fila is None:
        return None
    return convertir_pelicula(fila)


def ultimas_peliculas():
    cursor = connection.cursor()
    cursor.execute(
        "SELECT p.id_pelicula, p.titulo, p.nacionalidad, p.productora, "
        "p.anio, d.nombre "
        "FROM pelicula p "
        "LEFT JOIN director d ON p.id_director = d.id_director "
        "ORDER BY p.id_pelicula DESC LIMIT 5"
    )
    peliculas = []
    for fila in cursor.fetchall():
        peliculas.append(convertir_pelicula(fila))
    return peliculas


def convertir_pelicula(fila):
    return {
        'pk': fila[0],
        'titulo': fila[1],
        'nacionalidad': fila[2],
        'productora': fila[3],
        'anio': fila[4],
        'director': fila[5] or 'Sin director',
        'ejemplares': contar_ejemplares(fila[0]),
    }


def crear_pelicula(titulo, nacionalidad, productora, anio, id_director):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO pelicula (titulo, nacionalidad, productora, anio, id_director) "
        "VALUES (%s, %s, %s, %s, %s)",
        [titulo, nacionalidad, productora, anio, id_director],
    )
    pelicula_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO ejemplar (numero_ejemplar, estado, id_pelicula) "
        "VALUES (1, 'Disponible', %s)",
        [pelicula_id],
    )


def actualizar_pelicula(pelicula_id, titulo, nacionalidad, productora, anio, id_director):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE pelicula SET titulo = %s, nacionalidad = %s, productora = %s, "
        "anio = %s, id_director = %s WHERE id_pelicula = %s",
        [titulo, nacionalidad, productora, anio, id_director, pelicula_id],
    )


def eliminar_pelicula(pelicula_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM pelicula WHERE id_pelicula = %s", [pelicula_id])


def pelicula_tiene_ejemplares(pelicula_id):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM ejemplar WHERE id_pelicula = %s",
        [pelicula_id],
    )
    return cursor.fetchone()[0] > 0


def contar_ejemplares(pelicula_id):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM ejemplar WHERE id_pelicula = %s",
        [pelicula_id],
    )
    return cursor.fetchone()[0]


def todos_los_socios():
    cursor = connection.cursor()
    cursor.execute(
        "SELECT s.dni, s.nombre, s.direccion, s.telefono, "
        "s.avalador_dni, a.nombre "
        "FROM socio s "
        "LEFT JOIN socio a ON s.avalador_dni = a.dni "
        "ORDER BY s.nombre"
    )
    socios = []
    for fila in cursor.fetchall():
        socios.append({
            'pk': fila[0],
            'dni': fila[0],
            'nombre': fila[1],
            'direccion': fila[2],
            'telefono': fila[3],
            'avalador_dni': fila[4],
            'avalador': fila[5],
            'alquileres_activos': contar_alquileres_socio(fila[0]),
        })
    return socios


def socio_por_id(dni):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT s.dni, s.nombre, s.direccion, s.telefono, s.avalador_dni "
        "FROM socio s WHERE s.dni = %s",
        [dni],
    )
    fila = cursor.fetchone()
    if fila is None:
        return None
    return {
        'pk': fila[0],
        'dni': fila[0],
        'nombre': fila[1],
        'direccion': fila[2],
        'telefono': fila[3],
        'avalador_dni': fila[4],
    }


def crear_socio(dni, nombre, direccion, telefono, avalador_dni):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO socio (dni, nombre, direccion, telefono, avalador_dni) "
        "VALUES (%s, %s, %s, %s, %s)",
        [dni, nombre, direccion, telefono, avalador_dni],
    )


def actualizar_socio(dni, nombre, direccion, telefono, avalador_dni):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE socio SET nombre = %s, direccion = %s, telefono = %s, "
        "avalador_dni = %s WHERE dni = %s",
        [nombre, direccion, telefono, avalador_dni, dni],
    )


def eliminar_socio(dni):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM socio WHERE dni = %s", [dni])


def existe_socio(dni):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM socio WHERE dni = %s", [dni])
    return cursor.fetchone()[0] > 0


def socio_tiene_alquileres(dni):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM alquiler WHERE dni_socio = %s",
        [dni],
    )
    return cursor.fetchone()[0] > 0


def contar_alquileres_socio(dni):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM alquiler "
        "WHERE dni_socio = %s AND fecha_devolucion IS NULL",
        [dni],
    )
    return cursor.fetchone()[0]


def todos_los_ejemplares():
    cursor = connection.cursor()
    cursor.execute(
        "SELECT e.id_ejemplar, e.numero_ejemplar, p.titulo "
        "FROM ejemplar e "
        "JOIN pelicula p ON e.id_pelicula = p.id_pelicula "
        "ORDER BY p.titulo, e.numero_ejemplar"
    )
    ejemplares = []
    for fila in cursor.fetchall():
        ejemplares.append({
            'pk': fila[0],
            'numero': fila[1],
            'pelicula': fila[2],
        })
    return ejemplares


def todos_los_alquileres():
    cursor = connection.cursor()
    cursor.execute(
        "SELECT al.id_alquiler, al.fecha_inicio, al.fecha_devolucion, "
        "s.dni, s.nombre, e.numero_ejemplar, p.titulo "
        "FROM alquiler al "
        "JOIN socio s ON al.dni_socio = s.dni "
        "JOIN ejemplar e ON al.id_ejemplar = e.id_ejemplar "
        "JOIN pelicula p ON e.id_pelicula = p.id_pelicula "
        "ORDER BY al.fecha_inicio DESC"
    )
    return convertir_alquileres(cursor.fetchall())


def alquileres_activos():
    cursor = connection.cursor()
    cursor.execute(
        "SELECT al.id_alquiler, al.fecha_inicio, al.fecha_devolucion, "
        "s.dni, s.nombre, e.numero_ejemplar, p.titulo "
        "FROM alquiler al "
        "JOIN socio s ON al.dni_socio = s.dni "
        "JOIN ejemplar e ON al.id_ejemplar = e.id_ejemplar "
        "JOIN pelicula p ON e.id_pelicula = p.id_pelicula "
        "WHERE al.fecha_devolucion IS NULL "
        "ORDER BY al.fecha_inicio DESC"
    )
    return convertir_alquileres(cursor.fetchall())


def convertir_alquileres(filas):
    alquileres = []
    for fila in filas:
        alquileres.append({
            'pk': fila[0],
            'fecha_inicio': fila[1],
            'fecha_devolucion': fila[2],
            'socio': fila[4],
            'ejemplar': 'Nº ' + str(fila[5]),
            'pelicula': fila[6],
        })
    return alquileres


def ultimos_alquileres():
    return todos_los_alquileres()[:5]


def alquiler_devuelto(alquiler_id):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT fecha_devolucion FROM alquiler WHERE id_alquiler = %s",
        [alquiler_id],
    )
    fila = cursor.fetchone()
    if fila is None:
        return None
    return fila[0] is not None


def crear_alquiler(dni_socio, id_ejemplar, fecha_inicio):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO alquiler (fecha_inicio, dni_socio, id_ejemplar) "
        "VALUES (%s, %s, %s)",
        [fecha_inicio, dni_socio, id_ejemplar],
    )


def devolver_alquiler(alquiler_id):
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE alquiler SET fecha_devolucion = CURRENT_DATE "
        "WHERE id_alquiler = %s",
        [alquiler_id],
    )


def total_peliculas():
    return contar('pelicula')


def total_socios():
    return contar('socio')


def total_ejemplares():
    return contar('ejemplar')


def contar(tabla):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM " + tabla)
    return cursor.fetchone()[0]


def total_alquileres(activos):
    cursor = connection.cursor()
    if activos:
        cursor.execute(
            "SELECT COUNT(*) FROM alquiler WHERE fecha_devolucion IS NULL"
        )
    else:
        cursor.execute(
            "SELECT COUNT(*) FROM alquiler WHERE fecha_devolucion IS NOT NULL"
        )
    return cursor.fetchone()[0]
