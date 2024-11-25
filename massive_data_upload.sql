-- Para la tabla Albumes

COPY Albumes(album_id, nombre, fecha_lanzamiento)
FROM 'C:\Users\Public\Downloads\Albumes.csv'
DELIMITER ',' CSV HEADER;

-- Para la tabla Canciones

COPY Canciones(spotify_id, nombre, es_explicito, duracion_ms, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, album_id)
FROM 'C:\Users\Public\Downloads\Canciones.csv'
DELIMITER ';' CSV HEADER;

-- Para la tabla Artistas

COPY Artistas(artista_id, nombre)
FROM 'C:\Users\Public\Downloads\Artistas.csv'
DELIMITER ';' CSV HEADER;

-- Para la tabla Cancion_Artista

COPY Cancion_Artista(spotify_id, artista_id)
FROM 'C:\Users\Public\Downloads\Cancion_Artista.csv'
DELIMITER ',' CSV HEADER;

-- Para la tabla Paises

COPY Paises(pais_codigo, nombre)
FROM 'C:\Users\Public\Downloads\Paises.csv'
DELIMITER ',' CSV HEADER;

-- Para la tabla Snapshots
COPY Snapshots(fecha_snapshot)
FROM 'C:\Users\Public\Downloads\Snapshots.csv'
DELIMITER ',' CSV HEADER;

-- Para la tabla Rankings

COPY Rankings(spotify_id, pais_codigo, fecha_snapshot, ranking_diario, movimiento_diario, movimiento_semanal)
FROM 'C:\Users\Public\Downloads\Rankings.csv'
DELIMITER ',' CSV HEADER;