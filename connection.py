import psycopg2
try:
    connection = psycopg2.connect(
        host='localhost',
        user='postgres', # Usuario de la base de datos (Cambiar si es necesario)
        password='1234567890', # Contraseña de la base de datos (Cambiar si es necesario)
        database='spotify_db'
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

    # Consulta #1: tabla Albumes
    cursor = connection.cursor()
    cursor.execute(t_Albumes)
    rows = cursor.fetchall()
    print('TABLA ALBUMES: album_id, nombre, fecha_lanzamiento')
    for row in rows:
        print(row)
    print("\n")

    # Consulta #2: tabla Canciones
    cursor = connection.cursor()
    cursor.execute(t_Canciones)
    rows = cursor.fetchall()
    print('TABLA CANCIONES: spotify_id, nombre, popularidad, es_explicito, duracion_ms, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, album_id')
    for row in rows:
        print(row)
    print("\n")

    # Consulta #3: tabla Artistas
    cursor = connection.cursor()
    cursor.execute(t_Artistas)
    rows = cursor.fetchall()
    print('TABLA ARTISTAS: artista_id, nombre')
    for row in rows:
        print(row)
    print("\n")

    # Consulta #4: tabla Cancion_Artista
    cursor = connection.cursor()
    cursor.execute(t_Cancion_Artista)
    rows = cursor.fetchall()
    print('TABLA CANCION_ARTISTA: spotify_id, artista_id')
    for row in rows:
        print(row)
    print("\n")

    # Consulta #5: tabla Paises
    cursor = connection.cursor()
    cursor.execute(t_Paises)
    rows = cursor.fetchall()
    print('TABLA PAISES: pais_codigo, nombre')
    for row in rows:
        print(row)
    print("\n")

    # Consulta #6: tabla Snapshots
    cursor = connection.cursor()
    cursor.execute(t_Snapshots)
    rows = cursor.fetchall()
    print('TABLA SNAPSHOTS: fecha_snapshot')
    for row in rows:
        print(row)
    print("\n")

    # Consulta #7: tabla Rankings
    cursor = connection.cursor()
    cursor.execute(t_Rankings)
    rows = cursor.fetchall()
    print('TABLA RANKINGS: spotify_id, pais_codigo, fecha_snapshot, ranking_diario, movimiento_diario, movimiento_semanal')
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