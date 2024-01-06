# FUNCIONES A PARA LOS ENDPOINTS 
# Este archivo contiene las funciones para los endpoints que se consumirán en la API.
# Son las funciones que se definieron en el notebook 'Funciones_endpoints.ipynb'
# Se creó este archivo para facilitar su ejecución con fastapi y no sobrecargarlo.
# Asegurarse que los archivos .CSV input esten en la misma carpeta que este archivo

#=================================== LIBRERÍAS ===========================================
import pandas as pd

#=================================== FUNCIONES ===========================================

# ENDPOINT 1
# def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
# Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

def PlayTimeGenre(genero: str):
    df = pd.read_csv('PlayTimeGenre.csv')
    
    # Agrupa por género y encuentra el índice (idxmax()) correspondiente fila con el  valor máximo en la columna 'hours_game' para cada grupo
    max_indices = df.groupby('genres')['Hours_played'].idxmax()

    # Seleccionar las filas correspondientes a los índices encontrados
    df_resultante = df.loc[max_indices]
    # Encuentra el año con la mayor cantidad de horas jugadas para un género específico
    year_max_Hours_played = df_resultante.loc[df_resultante['genres'] == genero, 'release_year'].iloc[0]
    
    # Construye el response_data
    rpta1 = {"Año de lanzamiento con más horas jugadas para Género '{}'"":" "{}".format(genero, year_max_Hours_played)}

    return rpta1


# ENDPOINT 2
# def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
# Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

def UserForGenre( genero:str ):
    df2 = pd.read_csv('UserForGenre.csv',low_memory=False)

    df2_genre = df2[df2['genres']==genero]
    # Agrupar por 'genres', 'user_id' y 'release_year' y sumar 'Hours_played'
    df3_genre = df2_genre.groupby(['genres', 'user_id'], as_index=False)['Hours_played'].sum()
   
    # Encuentra el índice del usuario con el máximo número de Hours_played
    indice_max_hours = df3_genre['Hours_played'].idxmax()
    # Obtiene el user_id con mayor 'Hours_played' para el genero indicado
    user_id_max_hours = df3_genre.loc[indice_max_hours, 'user_id']

    df2_genre = df2_genre[df2_genre['user_id']==user_id_max_hours]
    # Filtra por 'user_id' igual al user_id con maximo numeor de horas jugadas y selecciona las columnas 'release_year' y 'Hours_played'
    df2_genre1 = df2_genre[df2_genre['user_id']==user_id_max_hours][['release_year', 'Hours_played']]
    
    # Actualiza nombre de columnas
    df2_genre1 = df2_genre1.rename(columns={'release_year': 'Año', 'Hours_played': 'Horas'})

    # Listamos como diccionario las 'Hours_played' por año
    dict_year_hours = df2_genre1.to_dict(orient='records') #  'records' significa que cada fila del DataFrame se convertirá en un diccionario

    # Crea el diccionario de retorno
    rpta2 = {
        "Usuario con más horas jugadas para Género {}".format(genero): user_id_max_hours,
        "Horas jugadas": dict_year_hours}

    return rpta2


# ENDPOINT 3
# def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
# Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

def UsersRecommend(anio: int):
    df3 = pd.read_csv('UsersRecommend.csv')
    
    # Filtra por el año indicado
    df3_year = df3[df3['year']==anio]
    
    # selecciona las tres filas con los valores mayores en la columna 'number_user_id_recom'
    df3_year_top3 = df3_year.nlargest(3, 'number_user_id_recom')

    # Armamos la estuctura de respuesta
    rpta3 = [{"Puesto 1": df3_year_top3.iloc[0]['app_name']},{"Puesto 2": df3_year_top3.iloc[1]['app_name']},{"Puesto 3": df3_year_top3.iloc[2]['app_name']}]

    return rpta3


# ENDPOINT 4
# def UsersWorstDeveloper( año : int ): Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
# Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

def UsersWorstDeveloper( anio : int ):
    df4 = pd.read_csv('UsersWorstDeveloper.csv')
    
    # Filtra por el año indicado
    df4_year = df4[df4['year']==anio]
    
    # Ordena de forma ascendente según la columna 'number_user_id_recom' y developer
    sorted_df = df4_year.sort_values(by=['number_user_id_norecom', 'developer'])
    # Elimina duplicados de 'developer', manteniendo la primera ocurrencia, esto se hace para no repetir de desarrolladora
    unique_developers = sorted_df.drop_duplicates(subset='developer', keep='first')
    # selecciona las tres filas con los valores más bajos en la columna 'number_user_id_recom'
    df4_year_top3_developers = unique_developers.head(3)

    # Armamos la estuctura de respuesta
    rpta4 = [{"Puesto 1": df4_year_top3_developers.iloc[0]['developer']},{"Puesto 2": df4_year_top3_developers.iloc[1]['developer']},{"Puesto 3": df4_year_top3_developers.iloc[2]['developer']}]

    return rpta4 


# ENDPOINT 5
# def sentiment_analysis( empresa desarrolladora : str ): Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
# Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}

def sentiment_analysis(empresa_desarrolladora: str):
    df5 = pd.read_csv('sentiment_analysis.csv')
    #Filtra por empresa desarrolladora
    df_5_1 = df5[df5['developer']==empresa_desarrolladora]
    # Guarda como diccionario la fila seleccionada
    rpta5= df_5_1.set_index('developer').to_dict(orient='index')
    #Se da el formato para la respuesta
    #rpta5= {row['developer']: [f"Negative = {row['Negative']}", f"Neutral = {row['Neutral']}", f"Positive = {row['Positive']}"] for index, row in df_5_1.iterrows()}

    return rpta5


# ENDPOINT 6
# MODELO DE APRENDIZAJE AUTOMÁTICO: SISTEMA DE RECOMENDACIÓN
