import psycopg2
try:
    connection = psycopg2.connect(
        host='localhost',
        user='postgres', # Usuario de la base de datos (Cambiar si es necesario)
        password='2I@@`7ao*3}*', # Contraseña de la base de datos (Cambiar si es necesario)
        database='proyecto'
    )
    print("Conexión exitosa")

    # Asignación de las tablas a variables
    t_Albumes = "select * from Albumes"
    t_Canciones = "select * from Canciones"
    t_Artistas = "select * from Artistas"
    t_Cancion_Artista = "select * from Cancion_Artista"
    t_Paises = "select * from Paises"
    t_Snapshots = "select * from Snapshots"
    t_Rankings = "select * from Rankings"

    #Asignación de las consultas a variables

    # Consulta 1: Impacto de atributos musicales en el éxito.
    t_consulta1 = "SELECT c.nombre AS cancion, r.pais_codigo, r.ranking_diario, r.movimiento_diario, r.movimiento_semanal, c.danceability, c.energy, c.tempo FROM Rankings r JOIN Canciones c ON r.spotify_id = c.spotify_id WHERE r.movimiento_diario IS NOT NULL AND r.movimiento_diario > 0 OR r.movimiento_semanal IS NOT NULL AND r.movimiento_semanal > 0 ORDER BY r.movimiento_diario DESC, r.movimiento_semanal DESC;"
    # Consulta 2: Canciones más populares por artista.
    t_consulta2 = "SELECT c.nombre AS cancion, p.nombre AS pais, MAX(r.ranking_diario) AS mejor_posicion, COUNT(r.fecha_snapshot) AS veces_en_ranking FROM Rankings r JOIN Canciones c ON r.spotify_id = c.spotify_id JOIN Paises p ON r.pais_codigo = p.pais_codigo GROUP BY c.nombre, p.nombre ORDER BY veces_en_ranking DESC, mejor_posicion ASC;"
    # Consulta 3: Tendencias temporales de popularidad.
    t_consulta3 = "SELECT p.nombre AS pais, c.nombre AS cancion, AVG(r.ranking_diario) AS promedio_ranking, MAX(r.movimiento_diario) AS max_movimiento_diario, MAX(r.movimiento_semanal) AS max_movimiento_semanal, AVG(c.danceability) AS promedio_danceability, AVG(c.energy) AS promedio_energy, AVG(c.tempo) AS promedio_tempo FROM Rankings r JOIN Canciones c ON r.spotify_id = c.spotify_id JOIN Paises p ON r.pais_codigo = p.pais_codigo GROUP BY p.nombre, c.nombre ORDER BY promedio_ranking ASC, max_movimiento_diario DESC;"
    # Consulta 4: Diversidad musical y número de artistas por país.
    t_consulta4 = "SELECT p.nombre AS pais, AVG(c.energy) AS promedio_energy, AVG(c.danceability) AS promedio_danceability, AVG(c.tempo) AS promedio_tempo, COUNT(DISTINCT r.spotify_id) AS cantidad_canciones FROM Rankings r JOIN Canciones c ON r.spotify_id = c.spotify_id JOIN Paises p ON r.pais_codigo = p.pais_codigo GROUP BY p.nombre ORDER BY cantidad_canciones DESC;"

    # Tabla Albumes
    cursor = connection.cursor()
    cursor.execute(t_Albumes)
    rows = cursor.fetchall()
    print('TABLA ALBUMES: album_id, nombre, fecha_lanzamiento')
    for row in rows:
        print(row)
    print("\n")

    # Tabla Canciones
    cursor = connection.cursor()
    cursor.execute(t_Canciones)
    rows = cursor.fetchall()
    print('TABLA CANCIONES: spotify_id, nombre, es_explicito, duracion_ms, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, album_id')
    for row in rows:
        print(row)
    print("\n")

    # Tabla Artistas
    cursor = connection.cursor()
    cursor.execute(t_Artistas)
    rows = cursor.fetchall()
    print('TABLA ARTISTAS: artista_id, nombre')
    for row in rows:
        print(row)
    print("\n")

    # Tabla Cancion_Artista
    cursor = connection.cursor()
    cursor.execute(t_Cancion_Artista)
    rows = cursor.fetchall()
    print('TABLA CANCION_ARTISTA: spotify_id, artista_id')
    for row in rows:
        print(row)
    print("\n")

    # Tabla Paises
    cursor = connection.cursor()
    cursor.execute(t_Paises)
    rows = cursor.fetchall()
    print('TABLA PAISES: pais_codigo, nombre')
    for row in rows:
        print(row)
    print("\n")

    # Tabla Snapshots
    cursor = connection.cursor()
    cursor.execute(t_Snapshots)
    rows = cursor.fetchall()
    print('TABLA SNAPSHOTS: fecha_snapshot')
    for row in rows:
        print(row)
    print("\n")

    # Tabla Rankings
    cursor = connection.cursor()
    cursor.execute(t_Rankings)
    rows = cursor.fetchall()
    print('TABLA RANKINGS: spotify_id, pais_codigo, fecha_snapshot, ranking_diario, movimiento_diario, movimiento_semanal')
    for row in rows:
        print(row)
    print("\n")

    # Consulta 1
    cursor = connection.cursor()
    cursor.execute(t_consulta1)
    rows = cursor.fetchall()
    print('CONSULTA 1: cancion, pais_codigo, ranking_diario, movimiento_diario, movimiento_semanal, danceability, energy, tempo')
    for row in rows:
        print(row)
    print("\n")
    
    # Consulta 2
    cursor = connection.cursor()
    cursor.execute(t_consulta2)
    rows = cursor.fetchall()
    print('CONSULTA 2: cancion, pais, mejor_posicion, veces_en_ranking')
    for row in rows:
        print(row)
    print("\n")
    
    # Consulta 3
    cursor = connection.cursor()
    cursor.execute(t_consulta3)
    rows = cursor.fetchall()
    print('CONSULTA 3: pais, cancion, promedio_ranking, max_movimiento_diario, max_movimiento_semanal, promedio_danceability, promedio_energy, promedio_tempo')
    for row in rows:
        print(row)
    print("\n")
    
    # Consulta 4
    cursor = connection.cursor()
    cursor.execute(t_consulta4)
    rows = cursor.fetchall()
    print('CONSULTA 4: pais, promedio_energy, promedio_danceability, promedio_tempo, cantidad_canciones')
    for row in rows:
        print(row)
    print("\n")

# Manejo de errores
except Exception as error:
    print("Error al conectar a la base de datos", error)
# Cerrar la conexión
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Conexión cerrada")