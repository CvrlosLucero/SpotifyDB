-- Active: 1730523126804@@127.0.0.1@5432@mi_base_de_datos
-- Tabla Albumes
CREATE TABLE Albumes (
    album_id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    fecha_lanzamiento DATE NOT NULL
);

-- Tabla Canciones
CREATE TABLE Canciones (
    spotify_id VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    popularidad INTEGER CHECK (popularidad BETWEEN 0 AND 100),
    es_explicito BOOLEAN NOT NULL,
    duracion_ms INTEGER NOT NULL,
    danceability NUMERIC(3,2) CHECK (danceability BETWEEN 0.0 AND 1.0),
    energy NUMERIC(3,2) CHECK (energy BETWEEN 0.0 AND 1.0),
    key INTEGER,
    loudness NUMERIC(5,2),
    mode INTEGER,
    speechiness NUMERIC(3,2) CHECK (speechiness BETWEEN 0.0 AND 1.0),
    acousticness NUMERIC(3,2) CHECK (acousticness BETWEEN 0.0 AND 1.0),
    instrumentalness NUMERIC(3,2) CHECK (instrumentalness BETWEEN 0.0 AND 1.0),
    liveness NUMERIC(3,2) CHECK (liveness BETWEEN 0.0 AND 1.0),
    valence NUMERIC(3,2) CHECK (valence BETWEEN 0.0 AND 1.0),
    tempo NUMERIC(5,2),
    time_signature INTEGER,
    album_id INTEGER REFERENCES Albumes(album_id)
);

-- Tabla Artistas
CREATE TABLE Artistas (
    artista_id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

-- Tabla Cancion_Artista
CREATE TABLE Cancion_Artista (
    spotify_id VARCHAR(50) REFERENCES Canciones(spotify_id),
    artista_id INTEGER REFERENCES Artistas(artista_id),
    PRIMARY KEY (spotify_id, artista_id)
);

-- Tabla Paises
CREATE TABLE Paises (
    pais_codigo CHAR(2) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla Snapshots
CREATE TABLE Snapshots (
    fecha_snapshot DATE PRIMARY KEY
);

-- Tabla Rankings
CREATE TABLE Rankings (
    spotify_id VARCHAR(50) REFERENCES Canciones(spotify_id),
    pais_codigo CHAR(2) REFERENCES Paises(pais_codigo),
    fecha_snapshot DATE REFERENCES Snapshots(fecha_snapshot),
    ranking_diario INTEGER NOT NULL CHECK (ranking_diario > 0),
    movimiento_diario INTEGER,
    movimiento_semanal INTEGER,
    PRIMARY KEY (spotify_id, pais_codigo, fecha_snapshot)
);
