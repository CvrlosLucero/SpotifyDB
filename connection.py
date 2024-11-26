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
    t_consulta1 = "SELECT c.spotify_id, c.nombre AS cancion, c.danceability, c.energy, c.valence, c.tempo, MIN(r.ranking_diario) AS mejor_ranking FROM Canciones c JOIN Rankings r ON c.spotify_id = r.spotify_id GROUP BY c.spotify_id, c.nombre, c.danceability, c.energy, c.valence, c.tempo HAVING MIN(r.ranking_diario) <= 10 ORDER BY mejor_ranking ASC;"
    # Consulta 2: Canciones más populares por artista.
    t_consulta2 = "SELECT a.nombre AS artista, c.nombre AS cancion, MIN(r.ranking_diario) AS mejor_posicion FROM Artistas a JOIN Cancion_Artista ca ON a.artista_id = ca.artista_id JOIN Canciones c ON ca.spotify_id = c.spotify_id JOIN Rankings r ON c.spotify_id = r.spotify_id GROUP BY a.nombre, c.nombre ORDER BY mejor_posicion ASC, a.nombre;"
    # Consulta 3: Tendencias temporales de popularidad.
    t_consulta3 = "SELECT c.nombre AS cancion, s.fecha_snapshot, AVG(r.ranking_diario) AS promedio_ranking FROM Canciones c JOIN Rankings r ON c.spotify_id = r.spotify_id JOIN Snapshots s ON r.fecha_snapshot = s.fecha_snapshot GROUP BY c.nombre, s.fecha_snapshot ORDER BY c.nombre, s.fecha_snapshot;"
    # Consulta 4: Diversidad musical y número de artistas por país.
    t_consulta4 = "SELECT p.nombre AS pais, COUNT(DISTINCT a.artista_id) AS cantidad_artistas, AVG(c.acousticness) AS promedio_acousticness, AVG(c.instrumentalness) AS promedio_instrumentalness, STDDEV(c.danceability) AS desviacion_danceability, STDDEV(c.energy) AS desviacion_energy FROM Rankings r JOIN Canciones c ON r.spotify_id = c.spotify_id JOIN Paises p ON r.pais_codigo = p.pais_codigo JOIN Cancion_Artista ca ON c.spotify_id = ca.spotify_id JOIN Artistas a ON ca.artista_id = a.artista_id GROUP BY p.nombre ORDER BY cantidad_artistas DESC, p.nombre;"

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