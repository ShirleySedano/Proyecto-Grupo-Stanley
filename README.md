## Actualización de la herramienta de visualización de los datos históricos y futuros a corto plazo y mediano plazo del S&P500 y sus principales componentes, que mejore la toma de decisiones oportunas con respecto a los portafolios de inversión del Grupo Stanley

##### Integrantes del proyecto:
* Andrés Parra Garzón
* Shirley Sánchez Sedano
* Viviana Vales

El mercado de valores en el que se negocian diferentes tipos de capitales alrededor del mundo permite
la canalización del capital a corto, mediano y largo plazo de los inversionistas, esperando
rentabilidades y beneficios mucho mayores a los que se obtienen en inversiones tradicionales en la
banca y en otros tipos de inversiones. En la medida en que un mercado tenga un mejor
posicionamiento se hace más atractivo para los inversionistas, razón por la cual el análisis de sus
comportamientos ha tomado gran interés y mayor relevancia a lo largo del tiempo.

El Grupo Stanley, es un consorcio financiero creado hace 50 años con presencia en más de 10 países de
Latinoamérica y que se dedica principalmente a ofrecer soluciones a los gobiernos, corporaciones y
privados en temas relacionados con inversiones, gestión patrimonial, finanzas corporativas y mercado
de capitales, reconoce la importancia de aprovechar la información para entregar herramientas a su
equipo de trabajo que permitan optimizar su gestión buscando así mejorar sus indicadores de
rentabilidad y satisfacción de clientes a través de la toma de mejores decisiones de inversión y
desinversión, indicadores que se han visto afectados es los últimos años y razón por la cual se decide hallar los 
mejores modelos para pronósticar de la manera más precisa los valores a corto plazo del S&P500 y las acciones del portafolio de la empresa. Actualmente, el grupo se encuentra interesado en consolidar una herramienta que le

##### Pregunta a resolver en nuestro proyecto:
¿Qué decisiones de inversión/desinversión debería tomar la Mesa de Dinero del grupo Stanley sobre su portafolio actual en el corto plazo?

### Proceso a realizar
1. Descarga de la información
2. Análisis descriptivo de los datos disponibles
3. Selección de modelos para predicciones del S&P500
4. Implementación de modelos y análisis de resultados para S&P500
5. Implementación de modelos para predecir acciones de MSTF y BRK.B
6. Implementación de modelos para predecir Betas de las acciones

### 1. Descarga de la información

Los rendimientos logaritmicos de los precios de cierre de las acciones del portafolio del grupo Stanley, más dos adicionales:

* SP500 
* Apple (AAPL) 
* Microsoft (MSFT)  
* Amazon (AMZN)  
* Tesla (TSLA) 
* Alphabet Class A (GOOGL)  
* Alphabet Class C (GOOG) 
* NVIDIA Corporation (NVDA) 
* Berkshire Hathaway Class B (BRK.B)  
* Meta (FB), formerly Facebook, Class A (META) 
* UnitedHealth Group (UNH) 
* Jhonson y Johnson (JNJ) 
* Procter & Gamble (PG) 
* Índice de Sentimiento del Mercado (VIX)

La información se extrae desde la API de Yahoo Finance desde el 2012-05-18 hasta el 2023-02-28.

Para observar el tratamiento previo que se le realizó a la información, dirigirse al siguiente enlace https://github.com/ShirleySedano/Proyecto-Grupo-Stanley/blob/main/ArregloBase.Rmd


### 2. Análisis descriptivo de los datos disponibles

### 3.	Selección de modelos y pruebas de verificación de los supuestos requeridos para usar los modelos elegidos.

Se realizaron las pruebas de Dickey Fuller,	Contraste de causalidad en el sentido de Granger y la identificación de variables más importantes a través de la función tsfeatures. 

En general se concluye de las dos primeras pruebas que los resultados de cada variable y sus rezagos pueden predecir de manera bidireccional de las demás variables. Por lo demostrado anteriormente se concluye que el modelo VAR es adecuado para nuestro proyecto.

En relación con los resultados de la función tsfeatures, encontramos que nos muestran que tenemos una serie con baja linealidad y alta entropía, lo cual hace que tenga características que la hacen difícil de pronosticar, y nos lleva a deducir que modelos lineales no se ajustarán muy bien a los datos. Por tanto, emplearemos modelos tipo Data Based como Redes Neuronales “LSTM” y Modelos de Ensamble como Random Forest que son propios para series con alta entropía. 


##### LSTM
La LSTM (Long-Short Term Memory) son un tipo de red neuronal artificial, exactamente una extensión de las redes neuronales recurrentes (RNN) donde puede aprender dependencias a largo plazo entre unidades de tiempo de datos secuenciales, es decir las LSTM permiten a las RNN recordar sus entradas durante un largo período. Los modelos intentados con este metodo se pueden observar 

##### VAR
Estos modelos vectoriales autorregresivospueden considerarse una extensión de los modelos autorregresivos AR(p) y 
se utiliza cuando se quiere caracterizar las interacciones simultaneas entre un grupo de variables, por lo tanto, no existe 
una variable dependiente y un conjunto de variables independientes que intentan explicarla, si no que existe un sistema de 
ecuaciones constituido por un bloque de rezagos de cada una de las variables del modelo que presentan interacción entre sí.Los modelos
que se intentaron y la precisión de los mismos los puede ver https://github.com/ShirleySedano/Proyecto-Grupo-Stanley/blob/main/ModelosVAR.Rmd

##### FORECASTER AUTOREGRESOR CON RANDOM FOREST
El Forecaster Autoregresor funciona como una herramienta bastante útil para realizar predicciones de series de tiempo usando modelos de regresión que emplean valores anteriores de la serie temporal como datos de entrada. Tiene la ventaja de permitir la optimización de hiperparámetros a través de búsqueda de cuadrícula y además de ofrecer la posibilidad de personalizar sus métricas para validar el modelo. Adicionalmente, la funcionalidad de obtener intervalos de predicción y conocer la importancia de los predictores del modelo. 

Dado que cuando se trabaja por predicciones, generalmente se quiere predecir no solo un siguiente momento de la serie o step, si no varios, existen estratégicas que permiten generar predicciones de múltiples. Para esto, es importante tener en cuenta que para predecir el momento tn se requiere conocer el valor de tn-1, es decir, siempre se hace uno del valor del día anterior para predecir el día siguiente. A este proceso se le conoce como recursive forecasting y puede generarse fácilmente a través de las clases ForecasterAutoreg y ForecasterAutoregCustom de skforecast. Random Forest proporciona ventajas al ser uno de los algoritmos de aprendizaje que corre eficientemente para grandes cantidades de datos con alto volumen de variables, permite entender cuáles son las variables más importantes dentro del modelo y ha demostrado altos niveles de precisión en el uso de series temporales.

### 4. Implementación de modelos y análisis de resultados para S&P500

##### LSTM


##### MODELOS VAR


##### FORECASTER AUTOREGRESOR CON RANDOM FOREST
Los resultados de la implementación de este modelo presentaron un muy buen desempeño, comparado con los resultados de los modelos VAR y LSTM. Se realizó la calibración de hiperparámetros y se hicieron varios experimentos que permitieron obtener un modelo óptimo para la predicción del S&P500. 

Sin embargo, nos encontramos con la necesidad de entrenar dos modelos adicionales para la predicción de los comportamietnos de dos de las acciones del portafolio, que se vincularon al modelo. Esto incremnentó sustancialmente el desempeño del modelo y por tanto, se consideró pertinente incluir estos dos modelos adicionales en el proyecto.

Los resultados de la implementación de este modelo se pueden consultar en el siguiente enlace 
https://github.com/ShirleySedano/Proyecto-Grupo-Stanley/blob/main/SkForecaster%20S%26P500.ipynb

### 5. Implementación de modelos para predecir acciones de MSTF y BRK.B

##### MSFT: 
Para realizar la predicción de los rendimientos logarítmicos de la acción de Microsoft se usa el modelo GARCH, el cual encuentra la volatilidad promedio a medio plazo mediante una autorregresión que depende de la suma de perturbaciones rezagadas y de la suma de varianzas rezagados. 

Los resultados los puede ver en https://github.com/ShirleySedano/Proyecto-Grupo-Stanley/blob/main/ModeloGARCH_MSFT.Rmd

##### BRK:

### 6. Implementación de modelos para predecir Betas de las acciones

##### Implementación de regresión lineal para la predicciones de los Betas de las acciones 

Para calcular los Betas se hace referencia al modelo de valoración de activos (CAPM) el cual permite estimar la rentabilidad esperada en función del riesgo sistemático.Para este proyecto se realiza de una regresión lineal simple y se calcula el valor de α y β teniendo en cuenta como variable independiente los rendimientos logarítmicos del S&P500 y la variable dependiente va variando por el resto de los rendimientos logarítmicos de las demás acciones contempladas en este trabajo.  El valor de α se refieren respectivamente a la valoración errónea del activo relativo al mercado, libre de riesgo, mientras que β indica la sensibilidad del riesgo del mercado. 

Los resultados los puede ver https://github.com/ShirleySedano/Proyecto-Grupo-Stanley/blob/main/Betas.ipynb


