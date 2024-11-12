-- Para la tabla Albumes

COPY Albumes(nombre, fecha_lanzamiento)
FROM '../albumes.csv'
DELIMITER ',' CSV HEADER;

-- Para la tabla Artistas

COPY Artistas(nombre)
FROM '../artistas.csv'
DELIMITER ',' CSV HEADER;

-- Para la tabla Canciones

COPY Canciones(spotify_id, nombre, popularidad, es_explicito, duracion_ms, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature, album_id)
FROM '../canciones.csv'
DELIMITER ',' CSV HEADER;

-- Para la tabla Cancion_Artista

COPY Cancion_Artista(spotify_id, artista_id)
FROM '../cancion_artista.csv'
DELIMITER ',' CSV HEADER;

-- Para la tabla Paises

COPY Paises(pais_codigo, nombre)
FROM '../paises.csv'
DELIMITER ',' CSV HEADER;

-- Para la tabla Snapshots
COPY Snapshots(fecha_snapshot)
FROM '../snapshots.csv'
DELIMITER ',' CSV HEADER;

-- Para la tabla Rankings

COPY Rankings(spotify_id, pais_codigo, fecha_snapshot, ranking_diario, movimiento_diario, movimiento_semanal)
FROM '../rankings.csv'
DELIMITER ',' CSV HEADER;