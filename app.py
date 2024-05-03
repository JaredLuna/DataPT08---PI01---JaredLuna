from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel


app = FastAPI()

@app.get('/')
def index():
    return {'Primer PI para Henry Data Science. By: JaredLuna'}

def load_data():
    df_steam_games = pd.read_parquet('./DataParquet/SteamGames.parquet')
    df_australian_items_ids = pd.read_parquet('./DataParquet/AustItems.parquet')
    df_australian_items_playtime = pd.read_parquet('./DataParquet/AustItemsExpand.parquet')
    df_reviews = pd.read_parquet('./DataParquet/CleanReviews.parquet')
    return df_steam_games,df_australian_items_ids,df_australian_items_playtime,df_reviews

@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre(genero: str):
    df_steam_games,df_australian_items_ids,df_australian_items_playtime,df_reviews = load_data()

    #Se nos va a dar una variables 'genero' a buscar
    tiene_genero = []

    for i in df_steam_games['genres']:
        for j in i:
            if genero.upper() == j.upper():
                tiene_genero.append('YES')
                break
            else:
                tiene_genero.append('NO')
                break

    df_steam_games['tiene_genero'] = tiene_genero
    #Hacemos un df nuevo de las filas que contienen el genero para obtener los IDS
    df_datos_con_genero = df_steam_games[df_steam_games['tiene_genero'].isin(['YES'])]
    df_datos_con_genero['id'] = df_datos_con_genero['id'].astype(int)
    Ids_con_genero = df_datos_con_genero['id'].astype(int).astype(str)

    #Encontramos las horas para los ids
    df_horas_id = df_australian_items_playtime[df_australian_items_playtime['item_id'].isin(Ids_con_genero)]

    #Creamos un dataframe con los ids y la sumas de sus horas
    df_suma_por_id = df_horas_id.groupby('item_id')['playtime_2weeks'].sum().reset_index()

    #Extramemos la fila que contenga el valor de horas mayor para obtener su ID
    indice_maximo = df_suma_por_id['playtime_2weeks'].idxmax()

    # Extraer la fila con el valor más alto
    fila_maximo = df_suma_por_id.loc[indice_maximo]
    IDfinal = fila_maximo['item_id']

    #Ya tenemos el Id con el mayor tiempo de horas jugadas para el genero propuesto, ahora es encontrar el año del juego que tiene ese id
    dato_final = df_datos_con_genero[df_datos_con_genero['id'].isin([int(IDfinal)])]

    #El resultado del año es:
    anio = dato_final['year']

    return {f'El año con más horas jugadas para el genero {genero.upper()}, es el año: {anio.values[0]}.'}

@app.get('/UserForGenre/{genero}')
def UserForGenre(genero: str):
    df_steam_games,df_australian_items_ids,df_australian_items_playtime,df_reviews = load_data()

    #Extraemos los datos de los generos coincidentes como en la primera función

    #Se nos va a dar una variables 'genero' a buscar
    tiene_genero = []

    for i in df_steam_games['genres']:
        for j in i:
            if genero.upper() == j.upper():
                tiene_genero.append('YES')
                break
            else:
                tiene_genero.append('NO')
                break

    df_steam_games['tiene_genero'] = tiene_genero

    #Apartamos nuestros datos del genero pedido
    df_datos_genero = df_steam_games[df_steam_games['tiene_genero'].isin(['YES'])]
    df_datos_genero['id'] = df_datos_genero['id'].astype(int).astype(str)

    #Ahora extraemos los id para poder encontrar el ID del usuario
    id_juegos = df_datos_genero['id']

    #Ahora separamos los datos de nuestros ids del dataframe playtime
    df_userIds_playtime = df_australian_items_playtime[df_australian_items_playtime['item_id'].isin(list(id_juegos))]

    #Obtenemos el jugador con más horas jugadas para el genero
    df_suma_por_id = df_userIds_playtime.groupby('user_id')['playtime_2weeks'].sum().reset_index()

    #Extramemos la fila que contenga el valor de horas mayor para obtener el id del user
    indice_maximo = df_suma_por_id['playtime_2weeks'].max()
    datos = df_suma_por_id[df_suma_por_id['playtime_2weeks'].isin([indice_maximo])]
    user = datos['user_id'].values[0]

    #Ya tenemos el usuario, así que ahora extraemos los juegos que ha jugado
    df_user_games_played = df_australian_items_playtime[df_australian_items_playtime['user_id'].isin([user])]
    juegos = df_user_games_played['item_id']

    #Ya tenemos los juegos, ahora hay que filtrarlos del df de genero y extraer los años que jugó
    df_user_games_played_per_year = df_datos_genero[df_datos_genero['id'].isin(juegos)]
    df_user_games_played_per_year = df_user_games_played_per_year.sort_values(by='year', ascending= True)
    años = df_user_games_played_per_year['year'].unique()

    #Ya tenemos los años, ahora buscamos los juegos por año en el df de generos, luegos esos ids hacemos las sumas de tiempo jugado y lo agregamos a una lista
    final = []
    for i in años:
        df_año_genero = df_datos_genero[df_datos_genero['year'].isin([i])]
        df_juego_x_año = df_user_games_played[df_user_games_played['item_id'].isin(df_año_genero['id'])]
        suma_horas = df_juego_x_año['playtime_2weeks'].sum()

        final.append(f'Año: {i}, Horas: {suma_horas/60}')

    return {f'Usuario con más horas jugadas para el genero {genero}: {user}\n{final}'}

@app.get('/UsersRecommend/{anio}')
def UsersRecommend(anio: int):
    df_steam_games,df_australian_items_ids,df_australian_items_playtime,df_reviews = load_data()

    anio = str(anio)

    #Extraemos los datos de los juegos para el año dado

    df_juego_año = df_steam_games[df_steam_games['year'].isin([anio])]
    df_juego_año['id'] = df_juego_año['id'].astype(int).astype(str)

    #Extraemos los IDs de los juegos
    Ids = df_juego_año['id']

    #Extraemos los datos de los juegos de ese año
    df_recomendacion_juegos_año = df_reviews[df_reviews['Item_Id'].isin(Ids)]

    #Extraemos los juegos más recomendado (calificación de 2)
    df_juegos_recomendados = df_recomendacion_juegos_año[df_recomendacion_juegos_año['sentiment_analysis'].isin([2 and 1])]

    #Obtenemos el jugador con más horas jugadas para el genero
    df_suma_por_id = df_juegos_recomendados.groupby('Item_Id')['sentiment_analysis'].sum().reset_index()
    df_suma_por_id = df_suma_por_id.sort_values(by= 'sentiment_analysis', ascending= False)

    #Extraemos el juego y las horas:
    id_game = []

    for i in df_suma_por_id[0:3].values:
        for j in i:
            if type(j) == int:
                continue
            else:
                id_game.append(j)

    #Ahora extraemos el nombre del juego para entregar la respuesta final
    titulos = []
    cont = 0
    for i in id_game:
        cont+= 1
        name = df_juego_año[df_juego_año['id'] == i]
        titulos.append('Puesto {}: {}'.format(cont, name.iloc[0]['title']))
    
    return {f'{titulos}'}

@app.get('/UsersNotRecommend/{anio}')
def UsersNotRecommend(anio: int):
    df_steam_games,df_australian_items_ids,df_australian_items_playtime,df_reviews = load_data()
    
    anio = str(anio)

    #Extraemos los datos de los juegos para el año dado

    df_juego_año = df_steam_games[df_steam_games['year'].isin([anio])]
    df_juego_año['id'] = df_juego_año['id'].astype(int).astype(str)

    #Extraemos los IDs de los juegos
    Ids = df_juego_año['id']

    #Extraemos los datos de los juegos de ese año
    df_recomendacion_juegos_año = df_reviews[df_reviews['Item_Id'].isin(Ids)]

    #Extraemos los juegos más recomendado (calificación de 2)
    df_juegos_recomendados = df_recomendacion_juegos_año[df_recomendacion_juegos_año['sentiment_analysis'].isin([0])]

    #Obtenemos el item id con un groupby
    df_suma_por_id = df_juegos_recomendados.groupby('Item_Id')['sentiment_analysis'].count().reset_index()
    df_suma_por_id = df_suma_por_id.sort_values(by= 'sentiment_analysis', ascending= False)

    #Extraemos el juego y las horas:
    id_game = []

    for i in df_suma_por_id[0:3].values:
        for j in i:
            if type(j) == int:
                continue
            else:
                id_game.append(j)

    #Ahora extraemos el nombre del juego para entregar la respuesta final
    titulos = []
    cont = 0
    for i in id_game:
        cont+= 1
        name = df_juego_año[df_juego_año['id'] == i]
        titulos.append('Puesto {}: {}'.format(cont, name.iloc[0]['title']))

    return {f'{titulos}'}

@app.get('/sentiment_analysis/{anio}')
def sentiment_analysis(anio : int):
    df_steam_games,df_australian_items_ids,df_australian_items_playtime,df_reviews = load_data()

    anio = str(anio)

    #Extraemos los ids de los juegos de ese año
    df_ids_año = df_steam_games[df_steam_games['year'].isin([anio])]
    ids_juegos = df_ids_año['id'].astype(int).astype(str)

    #Extraemos los sentiments analysis para esos ids
    df_ids_sentiment = df_reviews[df_reviews['Item_Id'].isin(ids_juegos)]

    #Creamos una nueva columna para clasificar si es buena, neutral o mala
    clasificacion = []
    for i in df_ids_sentiment['sentiment_analysis']:
        if i == 0:
            clasificacion.append('Negative')
        if i == 1:
            clasificacion.append('Neutral')
        if i == 2:
            clasificacion.append('Positive')

    df_ids_sentiment['Clasification'] = clasificacion
        
    #Creamos un DF para tener solo la columna de clasificación y sentimient
    datos = pd.DataFrame()
    datos['Clasificacion'] = df_ids_sentiment['Clasification']
    datos['sentiment_analysis'] = df_ids_sentiment['sentiment_analysis']

    #Ahora ordenamos
    df_suma_clasificacion = datos.groupby('Clasificacion')['sentiment_analysis'].count().reset_index()
    df_suma_clasificacion = df_suma_clasificacion.sort_values(by= 'sentiment_analysis', ascending= False)

    #Ordenamos nuestros datos para dar la respuesta final
    respuesta = []
    for i in df_suma_clasificacion.values:
        for j in i:
            respuesta.append(f'{i[0]} = {i[1]}')
            break
    
    return {f'{respuesta}'}