# DataPT08---PI01---JaredLuna

## PI_ML_OPS

Se nos plantea el desarrollar un proyecto MVP para la plataforma de videojuegos "Steam", donde se nos entregarán 3 datasets diferentes y con ellos hay que realizar una EDA, una ETL, unas funciones propuestas y finalmente realizar el deploy de nuestra API en render. Más adelante se explicarán a mayor detalle cada uno de los pasos.

## Exploratory Data Analysis (EDA)
Para la EDA se revisaron los 3 datasets, los cuales se encontraban en un formato “.json”. Este formato necesita una especial decodificación para poder ser visualizado. Una vez importados nuestros datos con pandas a dataframes pudimos observar que contábamos con muchos datos nulos para uno de nuestros datasets y en los otros dos pudimos notar que teníamos columnas con información anidada. Más detalles pueden ser encontrados dentro del jupyter notebook ‘EDA.ipynb’. 
Al final de la EDA conseguimos los siguientes insights:
1._ Para el dataset de steam games es necesario eliminar todos los datos vacíos y podemos ordenar los alfabéticamente los publishers para mayor orden
2._ Para el australian items es necesario desanidar la columna de items y así expandir nuestro dataframe
3._ Para el australian reviews es necesario hacer lo mismo, desanidar la columna de reviews y así expandir el dataframe para tener más datos.

## Extract Transform Load (ETL)
Para esta parte tomamos los insights que encontramos en al EDA y los empezamos a aplicar para cada uno de los datasets. La parte más complicada fue la desanidación de la información, pero lo más sencillo fue ir leyendo línea por línea con un ciclo FOR para ir tomando cada línea como una lista separada y así poder separar todo. Luego reemplazábamos ese valor con los resultados del ciclo FOR y listo, ya contamos con la información limpia en tipo listas para cada fila en dicha columna.
Posteriormente se realizaron pequeñas limpiezas de valores nulos y ordenamiento de la información para tenerla más prolija. Checamos al final todos los datos, separamos los que tenían columnas anidadas para tener un mejor orden y al final importamos todo a archivos con formato “.parquet”, esto con el fin de manejar la información en un formato más ligero y fácil de leer a la hora de importar nuestros datos a GitHub y posteriormente hacer el deploy en Render.

## Funciones
Pero antes de aplicar dichos insight primeramente nos centramos en nuestro sistema de ML con NLP para clasificar las reseñas de los usuarios. La clasificación se hizo estandarizó en valores numéricos donde:
Reseña buena = 2
Reseña neutral = 1
Reseña mala = 0
Esto para poder trabajar con valores numéricos y así poder hacer conteos de reseñas.
Esta parte fue interesante, ya que teníamos que entrenar nuestro modelo, para esto primeramente se empezó a clasificar varias de las reseñas de nuestro dataset para usarlo de tren de entrenamiento, sin embargo, nos dimos cuenta de que era perder demasiado tiempo y ni siquiera íbamos a conseguir un dataset de entrenamiento muy grande. Por lo tanto, se utilizó la a ChatGPT para ayudarnos con esta tarea. Se le pidió generar 100 reseñas positivas de videojuegos, 100 reseñas negativas y 100 reseñas neutrales, de esta manera logramos tener un tren de pruebas un poco más robusto y con esto entrenar a nuestro sistema de ML. Una vez generadas estas estas reseñas, se las dimos a nuestro sistema y al checar la precisión de este logramos casi una precisión del 80% en cada una de la identificación de las reseñas, un resultado bastante aceptable. Una vez entrenado nuestro sistema le pasamos nuestro data set de reviews para ser clasificado y así obtuvimos todas nuestras reseñas clasificadas.
Posteriormente a tener todas nuestras reviews clasificadas nos centramos a desarrollar las funciones que nos fueron propuestas, las cuales fueron:
- **def PlayTimeGenre(genero : str )**: Debe devolver año con más horas jugadas para dicho género.
- **def UserForGenre(genero : str )**: Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
- **def UsersRecommend(año : int )**: Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
- **def UsersNotRecommend(año : int )**: Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
- **def sentiment_analysis(año : int )**: Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
Para el desarrollo de todas las funciones solamente utilizamos pandas, primeramente, para la lectura de los archivos parquet junto con pyarrow y fastparquet. Y luego de importar toda la información y su transformación solamente fue necesaria la utilización de pandas.
La explicación de cada una de las funciones esta redactada en el jupyter notebook de “Funciones.ipynb”. No se ahondará más aquí en el readme, ya que se haría muy extensa la explicación.

## FastApi
Una vez realizadas las funciones y observar que están funcionando en nuestro notebook, nos podemos poner a realizar el main.py para darle formato para que FastApi sea capaz de leer nuestro código, compilarlo y correrlo localmente con uvicorn.
Para eso empezamos a declarar todas las funciones con el formato app.get(nombre_funcion), una vez definidas todas nuestras funciones guardamos nuestro archivo app.py (es el archivo main). Creamos el ambiente virutal, al cual importamos las librerías utilizadas en nuestro archivo main y así mediante CMD podemos generar el archivo requirements.txt con el comando:
“pip freeze > requirements.txt”
Una vez teniendo nuestro ambiente virtual y nuestros requerimientos, activiamos nuestro ambiente virtual y corremos nuestro script con uvicorn, con lo cual nos genera una ip que copiamos en nuestro navegador y podemos acceder a la documentación de nuestro script donde se encuentran todas las funciones desarrolladas. Al probar el funcionamiento localmente de las mismas nos pudimos dar cuenta que en la CMD aparecen los errores que tengamos, ya que al principio nos aparecieron errores con unas librerías que nos faltaban instalar, pero gracias a la CMD se pudo realizar el debug y solucionar los problemas. Una vez que todas nuestras funciones corren localmente sin problemas, se procedió a subir todo nuestro proyecto a GitHub para finalmente hacer el deploy en Render.

## Render Deploy
Para el deploy en render es necesario tener todo nuestro proyecto subido en GitHub, una vez ya teniendo todo ahí nos vamos a la pagina de Render y en dashboard escogimos la opción de “Web Service”. Posteriormente conectamos nuestra cuenta de GitHub con Render y hacemos el deploy de ese repositorio.
Si todo sale correctamente Render nos va a brindar un link el cual es el que se comparte para que cualquier persona pueda acceder a nuestra API desde cualquier parte del mundo. Revisamos que nuestras funciones estén funcionando correctamente en Render y con eso el deploy fue un éxito.
Con esto ya contamos con nuestro proyecto funcional y deployado. 

