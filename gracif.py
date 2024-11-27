import dash
from dash import html, dcc
import psycopg2
import pandas as pd
import plotly.express as px

# Configuración de la base de datos
DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_PASSWORD = '123456789'
DB_NAME = 'postgres'

# Conexión a la base de datos
def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para realizar consultas
def run_query(query):
    conn = get_connection()
    if conn is None:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return pd.DataFrame(rows, columns=column_names)
    except Exception as e:
        print(f"Error ejecutando la consulta: {e}")
        return None
    finally:
        conn.close()

# Consulta 1
def consulta_1():
    query = """
        SELECT c.spotify_id, c.nombre AS cancion, c.danceability, c.energy, 
               c.valence, c.tempo, MIN(r.ranking_diario) AS mejor_ranking
        FROM Canciones c
        JOIN Rankings r ON c.spotify_id = r.spotify_id
        GROUP BY c.spotify_id, c.nombre, c.danceability, c.energy, c.valence, c.tempo
        HAVING MIN(r.ranking_diario) <= 10
        ORDER BY mejor_ranking ASC;
    """
    return run_query(query)

# Consulta 2
def consulta_2():
    query = """
        SELECT a.nombre AS artista, c.nombre AS cancion, MIN(r.ranking_diario) AS mejor_posicion
        FROM Artistas a
        JOIN Cancion_Artista ca ON a.artista_id = ca.artista_id
        JOIN Canciones c ON ca.spotify_id = c.spotify_id
        JOIN Rankings r ON c.spotify_id = r.spotify_id
        GROUP BY a.nombre, c.nombre
        ORDER BY mejor_posicion ASC, a.nombre;
    """
    return run_query(query)

# Consulta 3
def consulta_3():
    query = """
        SELECT c.nombre AS cancion, s.fecha_snapshot, AVG(r.ranking_diario) AS promedio_ranking
        FROM Canciones c
        JOIN Rankings r ON c.spotify_id = r.spotify_id
        JOIN Snapshots s ON r.fecha_snapshot = s.fecha_snapshot
        GROUP BY c.nombre, s.fecha_snapshot
        ORDER BY c.nombre, s.fecha_snapshot
        LIMIT 50;
    """
    return run_query(query)

# Consulta 4
def consulta_4():
    query = """
        SELECT p.nombre AS pais, COUNT(DISTINCT a.artista_id) AS cantidad_artistas, 
               AVG(c.acousticness) AS promedio_acousticness, AVG(c.instrumentalness) AS promedio_instrumentalness, 
               STDDEV(c.danceability) AS desviacion_danceability, STDDEV(c.energy) AS desviacion_energy
        FROM Rankings r
        JOIN Canciones c ON r.spotify_id = c.spotify_id
        JOIN Paises p ON r.pais_codigo = p.pais_codigo
        JOIN Cancion_Artista ca ON c.spotify_id = ca.spotify_id
        JOIN Artistas a ON ca.artista_id = a.artista_id
        GROUP BY p.nombre
        ORDER BY cantidad_artistas DESC, p.nombre;
    """
    return run_query(query)

# Crear la app de Dash
app = dash.Dash(__name__)


app.layout = html.Div([
        dcc.Tabs([
            dcc.Tab(
                label='Consulta 1',
                children=[
                    html.H1("Mejor Ranking por Canción"),
                    html.Div([
                        html.P("""
                            En esta sección, se presenta la gráfica de barras generada a partir de los datos obtenidos de la consulta 1. 
                            Esta consulta analiza cómo los atributos musicales de las canciones, como danceability, energy, valence y tempo, 
                            están relacionados con su éxito en los rankings (definido por su mejor posición alcanzada).
                        """),
                        dcc.Graph(figure=px.bar(
                            consulta_1(),
                            x='cancion',
                            y='mejor_ranking',
                            title="Mejor Ranking por Canción",
                            labels={'mejor_ranking': 'Mejor Ranking', 'cancion': 'Canción'}
                        )),
                    ]),
                    html.Div([
                        html.H2("Análisis General"),
                        html.P("""
                            Si observamos rápidamente la lista, podemos notar que hay una variedad de artistas y géneros musicales representados. Sin embargo, parece haber una tendencia hacia la música urbana y el reggaetón, que son géneros muy populares en la actualidad. Además, podemos identificar algunas colaboraciones entre artistas de diferentes países, lo que refleja la globalización de la industria musical.
                        """),
                    ]),
                    html.Div([
                        html.H2("Análisis Particular"),
                        html.Ul([
                            html.Li("""
                                Muchos géneros "raqueados", como el rock, el punk o el metal, tienen una fuerte carga simbólica relacionada con la rebeldía, la independencia y el desafío a las normas establecidas. Esta música se asocia con movimientos juveniles que buscan expresar frustraciones o descontento hacia la sociedad, la política o las expectativas tradicionales. Es un medio para liberar emociones reprimidas, especialmente en un contexto de cambios culturales o políticos.
                            """),# TODO: carlos
                            html.Li(""" 
                                Se observa que las canciones que alcanzaron el Top 10 tienen características musicales similares, 
                                lo que podría indicar tendencias comunes en el gusto del público.
                            """),
                        ]),
                    ]),
                ]
            ),
            dcc.Tab(
                label='Consulta 2',
                children=[
                    html.H1("Mejor Posición de Canciones por Artista"),
                    html.Div([
                        html.P("""
                            En esta sección, se presenta la gráfica de barras generada a partir de los datos obtenidos de la consulta 2. 
                            Esta consulta encuentra la canción más exitosa de cada artista basándose en su mejor posición en los rankings.
                        """),
                        dcc.Graph(figure=px.bar(
                            consulta_2(),
                            x='artista',
                            y='mejor_posicion',
                            color='cancion',
                            title="Mejor Posición de Canciones por Artista",
                            labels={'mejor_posicion': 'Mejor Posición', 'artista': 'Artista', 'cancion': 'Canción'}
                        )),
                    ]),
                    html.Div([
                        html.H2("Análisis General"),
                        html.P("""
                            El gráfico presenta un panorama interesante sobre el desempeño de diversos artistas en términos de la mejor posición alcanzada por sus canciones en una determinada plataforma o lista musical. Se observa una gran variedad de artistas, predominantemente del género urbano y latino, con un rango amplio en las posiciones alcanzadas. Algunos artistas han logrado posicionarse en los primeros lugares, mientras que otros se encuentran en posiciones más bajas. Es evidente una competencia bastante reñida entre los artistas, con pequeñas variaciones en sus mejores posiciones.
                        """),
                    ]),
                    html.Div([
                        html.H2("Análisis Particular"),
                        html.Ul([
                            html.Li("""
                                La prevalencia de artistas de reguetón y música urbana en las primeras posiciones del gráfico sugiere una clara tendencia hacia estos géneros en la preferencia del público. Esto podría deberse a diversos factores como: Mayor producción y consumo,Conexión con el público, Competencia entre artistas
                            """), # TODO: carlos
                            html.Li("""
                                Los artistas con canciones en las mejores posiciones suelen estar asociados con géneros populares o 
                                tienen una base de fans amplia que impulsa su popularidad en los rankings.
                            """),
                        ]),
                    ]),
                ]
            ),
            dcc.Tab(
                label='Consulta 3',
                children=[
                    html.H1("Tendencias de Popularidad de Canciones a lo Largo del Tiempo"),
                    html.Div([
                        html.P("""
                            En esta sección, se presenta la gráfica de líneas a partir de los datos obtenidos de la consulta 3. 
                            Evalúa cómo varía la popularidad de las canciones a lo largo del tiempo observando su promedio de posición diaria (ranking_diario).
                        """),
                        dcc.Graph(figure=px.line(
                            consulta_3(),
                            x='fecha_snapshot',
                            y='promedio_ranking',
                            color='cancion',
                            title="Tendencias de Popularidad de Canciones a lo Largo del Tiempo",
                            labels={
                                'fecha_snapshot': 'Fecha',
                                'promedio_ranking': 'Promedio de Ranking',
                                'cancion': 'Canción'
                            }
                        )),
                    ]),
                    html.Div([
                        html.H2("Análisis General"),
                        html.P("""
                            El gráfico muestra la evolución del promedio de ranking de varias canciones a lo largo de un periodo de tiempo específico (del 17 al 24 de noviembre de 2024). Cada línea representa una canción diferente y su posición promedio en una determinada lista o ranking musical. Se observa una tendencia general de disminución en el ranking promedio para la mayoría de las canciones, lo que sugiere una posible pérdida de popularidad o disminución en la rotación en las listas. Sin embargo, hay algunas excepciones, como la canción representada por la línea verde, que muestra un ligero aumento en su ranking promedio.
                        """),
                    ]),
                    html.Div([
                        html.H2("Análisis Particular"),
                        html.Ul([
                            html.Li("""
                                la canción con línea morada experimenta una disminución constante en su ranking, indicando una pérdida gradual de popularidad. La canción con línea roja, por otro lado, mantiene un ranking relativamente estable durante la mayor parte del periodo, con una ligera disminución al final. En contraste, la canción con línea verde muestra un aumento gradual en su ranking, lo que sugiere un crecimiento en su popularidad. Las demás canciones presentan patrones mixtos, con algunas fluctuaciones en su ranking promedio, reflejando tanto subidas como bajadas en su desempeño.
                            """),# TODO: carlos
                            html.Li("""
                                Canciones con picos de popularidad: Otras canciones muestran incrementos significativos 
                                en popularidad en momentos específicos, lo que puede estar asociado a eventos promocionales 
                                o tendencias sociales.
                            """),
                        ]),
                    ]),
                ]
            ),
            dcc.Tab(
                label='Consulta 4',
                children=[
                    html.H1("Número de Artistas por País"),
                    html.Div([
                        html.P("""
                            En esta sección, se presenta la gráfica de barras a partir de los datos obtenidos de la consulta 4. 
                            Analiza la diversidad musical de cada país en términos de atributos como acousticness, 
                            instrumentalness y danceability, junto con la cantidad de artistas que contribuyen a esa diversidad.
                        """),
                        dcc.Graph(figure=px.bar(
                            consulta_4(),
                            x='pais',
                            y='cantidad_artistas',
                            title="Número de Artistas por País",
                            labels={'cantidad_artistas': 'Cantidad de Artistas', 'pais': 'País'}
                        )),
                    ]),
                    html.Div([
                        html.H2("Análisis General"),
                        html.P("""
                            El gráfico muestra una comparación de la cantidad de artistas musicales provenientes de seis países latinoamericanos: Ecuador, Argentina, Chile, Colombia, Costa Rica y México. Se observa que Ecuador presenta la mayor cantidad de artistas registrados, seguido de cerca por Argentina y Chile. Colombia, Costa Rica y México siguen esta tendencia, mostrando una cantidad menor pero significativa de artistas.
                        """),
                    ]),
                    html.Div([
                        html.H2("Análisis Particular"),
                        html.Ul([
                            html.Li("""
                                Ecuador se destaca como el país con el mayor número de artistas, lo cual podría explicarse por un mayor apoyo a la industria musical, mayor penetración de plataformas digitales que facilitan la difusión de la música ecuatoriana y una escena musical más activa y diversa. Por otro lado, Argentina, Chile y Colombia presentan números similares de artistas, lo que sugiere una escena musical regionalmente homogénea, influenciada por factores culturales, económicos y geográficos comunes. En cuanto a Costa Rica y México, aunque son países con una importante industria musical, su representación en los datos es menor. Esto podría deberse a criterios de selección que favorecieron a ciertos países o géneros, o a que la muestra de datos es limitada y no refleja completamente la industria musical en estos países.
                            """),# TODO: carlos
                            html.Li("""
                                Relación entre diversidad y atributos musicales: La variación en atributos como danceability y energy 
                                puede estar influenciada por la cantidad y diversidad de artistas en cada país, mostrando patrones culturales únicos.
                            """),
                        ]),
                    ]),
                ]
            ),
            dcc.Tab(
                label='Conclusiones',
                children=[
                    html.H1("Conclusiones Generales"),
                    html.Div([
                        html.P("""
                            A partir del análisis de las cuatro consultas presentadas, se pueden extraer varias conclusiones clave:
                        """),
                        html.H2("Tendencias Generales en el Éxito Musical"),
                        html.Ul([
                            html.Li("""
                                Las canciones que alcanzan las mejores posiciones en los rankings tienen características musicales similares, 
                                especialmente en géneros como el reggaetón y la música urbana, reflejando un patrón en las preferencias del público.
                            """),
                            html.Li("""
                                La música "raqueada", como el rock y el punk, sigue siendo relevante, especialmente en movimientos culturales juveniles, 
                                lo que muestra su valor simbólico y conexión emocional con ciertos grupos.
                            """),
                        ]),
                        html.H2("Éxito por Artista"),
                        html.Ul([
                            html.Li("""
                                Los artistas de reggaetón y música urbana dominan las primeras posiciones en los rankings, indicando una clara preferencia del público.
                            """),
                            html.Li("""
                                La diversidad en las posiciones de los artistas refleja una fuerte competencia en el ámbito musical, con pequeños márgenes de diferencia entre ellos.
                            """),
                        ]),
                        html.H2("Popularidad de las Canciones a lo Largo del Tiempo"),
                        html.Ul([
                            html.Li("""
                                La evolución del ranking promedio de las canciones muestra una tendencia general de disminución en su popularidad, aunque algunas canciones experimentan repuntes 
                                debido a eventos promocionales o tendencias sociales.
                            """),
                            html.Li("""
                                Canciones con comportamiento mixto en sus rankings resaltan cómo diferentes factores, como la promoción o cambios en la percepción pública, pueden impactar su éxito.
                            """),
                        ]),
                        html.H2("Diversidad y Representación de Artistas por País"),
                        html.Ul([
                            html.Li("""
                                Ecuador se destaca como el país con mayor número de artistas representados, posiblemente debido a un mayor apoyo institucional y penetración de plataformas digitales.
                            """),
                            html.Li("""
                                Países como Argentina, Chile y Colombia presentan una cantidad similar de artistas, sugiriendo homogeneidad regional en talento musical.
                            """),
                            html.Li("""
                                La relación entre diversidad musical de un país y atributos como danceability y energy muestra cómo la riqueza cultural influye en los estilos musicales predominantes.
                            """),
                        ]),
                        html.P("""
                            En resumen, el análisis resalta cómo los géneros urbanos y de reggaetón dominan el panorama musical actual, y la importancia de factores como la promoción, 
                            el acceso digital y la diversidad cultural en la popularidad y características de la música.
                        """),
                    ])
                ]
            )
        ])
    ],  
)

# Ejecutar el servidor
if __name__ == '__main__':
    app.run_server(debug=True)