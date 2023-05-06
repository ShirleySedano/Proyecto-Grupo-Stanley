## Actualización de la herramienta de visualización de los datos históricos y futuros a corto plazo y mediano plazo del S&P500 y sus principales componentes, que mejore la toma de decisiones oportunas con respecto a los portafolios de inversión del Grupo Stanley

## Reporte de selección y parametrización de modelos 

### Integrantes del proyecto:
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

### Pregunta a resolver en nuestro proyecto:
¿Qué decisiones de inversión/desinversión debería tomar la Mesa de Dinero del grupo Stanley sobre su portafolio actual en el corto plazo?

### Información con la que se va a trabajar:

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

La información se extrae desde la API de Yahoo Finance desde el 2012-05-18 hasta el 2023-02-28 

### Los tres mejores modelos detectados para pronosticar los rendimientos logaritmicos del S&P500:

#### LSTM:

#### VAR: Estos modelos vectoriales autorregresivospueden considerarse una extensión de los modelos autorregresivos AR(p) y 
se utiliza cuando se quiere caracterizar las interacciones simultaneas entre un grupo de variables, por lo tanto, no existe 
una variable dependiente y un conjunto de variables independientes que intentan explicarla, si no que existe un sistema de 
ecuaciones constituido por un bloque de rezagos de cada una de las variables del modelo que presentan interacción entre sí.Los modelos
que se intentaron y la precisión de los mismos los puede ver https://github.com/ShirleySedano/Proyecto-Grupo-Stanley/blob/main/ModelosVAR.Rmd

#### Forecaster Autoregresor de Skforercaster con Random Forest:

##### MSFT: 
Para realizar la predicción de los rendimientos logarítmicos de la acción de Microsoft se usa el modelo GARCH, el cual encuentra la volatilidad promedio a medio plazo mediante una autorregresión que depende de la suma de perturbaciones rezagadas y de la suma de varianzas rezagados. Los resultados los puede ver en https://github.com/ShirleySedano/Proyecto-Grupo-Stanley/blob/main/ModeloGARCH_MSFT.Rmd

#### BRK:


