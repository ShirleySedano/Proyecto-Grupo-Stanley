from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import joblib
import pickle
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
from datetime import datetime, timedelta,date
import tensorflow as tf
import keras

## Librerias necesarias

from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from pathlib import Path
import sys
home=str(Path.home()/ 'OneDrive - Florexpo\SP500')
sys.path.append(r'C:\Users\aparra\Anaconda3')
sys.path.append(r'C:\Users\aparra\Anaconda3\scripts')
sys.path.append(r'C:\Users\aparra\Anaconda3\Library\bin')
steps=7
delay=0


delay_table=pd.read_csv(home+"\MSFTStock\delay.csv")
delay_table.iat[0,0]=delay
delay_table.to_csv(home+"\MSFTStock\delay.csv",index=False)

delay_table=pd.read_csv(home+"\BRKStock\delay.csv")
delay_table.iat[0,0]=delay
delay_table.to_csv(home+"\BRKStock\delay.csv",index=False)

import os
os.environ["R_HOME"] = r"C:\Program Files\R\R-4.3.0" # change as needed
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import rpy2.robjects as ro
pandas2ri.activate()

def getMSFT():
    # Cargar el archivo "garch.R" en R
    robjects.r['source'](home+'\MSFTStock\MSFTModel.R')

    # Acceder a la función "mi_funcion" de R en Python
    mi_funcion = robjects.r['MSFT']
    MSFT=mi_funcion()
    MSFT = ro.conversion.rpy2py(MSFT)
    
    robjects.r['source'](home+'\BRKStock\BRBKModel.R')

    # Acceder a la función "mi_funcion" de R en Python
    mi_funcion = robjects.r['BRBK']
    BRBK=mi_funcion()
    BRBK = ro.conversion.rpy2py(BRBK)
    
    return MSFT,BRBK
pred_msft,pred_brk=getMSFT()

df = pd.concat([pred_msft.reset_index()[['simulacion']],pred_brk.reset_index()[['simulacion']]],axis=1)
df.columns = ['MSTF','BRK.B']

with open(home+'\SP500/SP500Scaler.gz', 'rb') as f:
    scaler = joblib.load(f)

with open(home+'\SP500/SP500Model', 'rb') as f:
    modelo = pickle.load(f)

columnas_scaler = ['GSPC.ReturnSuavizado', 'AAPL.ReturnSuavizado', 'AMZN.ReturnSuavizado',
       'MSTF.ReturnSuavizado', 'TSLA.ReturnSuavizado', 'GOOG.ReturnSuavizado',
       'GOOGL.ReturnSuavizado', 'NVDA.ReturnSuavizado',
       'BRK.B.ReturnSuavizado', 'META.ReturnSuavizado', 'UNH.ReturnSuavizado',
       'JNJ.ReturnSuavizado', 'PG.ReturnSuavizado', 'VIX.ReturnSuavizado',
       'DolarIndex.ReturnSuavizado']

df2 = pd.DataFrame(0, index=df.index, columns=columnas_scaler)
df2['BRK.B.ReturnSuavizado'] = df['BRK.B']
df2['MSTF.ReturnSuavizado'] = df['MSTF']
df2 = pd.DataFrame(scaler.transform(df2),columns=columnas_scaler,index=df.index)
exog = df2[['MSTF.ReturnSuavizado', 'BRK.B.ReturnSuavizado']] 

cur_date=date.today()- BDay(delay)
print(cur_date)
initial_date_SP=cur_date - BDay(20)

initial_date_SP=initial_date_SP.strftime('%Y-%m-%d')
print(initial_date_SP)

data_GSPC = pd.DataFrame(pdr.get_data_yahoo("^GSPC", initial_date_SP,cur_date)['Adj Close'])
log_returns=np.log(data_GSPC).diff()*100
log_returns=log_returns[1:]
log_returns.columns = ['GSPC']

yest_day=cur_date - BDay(1)
initial_date=cur_date - BDay(5)
final_date=cur_date + BDay(steps-1)
last_window_calendar=pd.bdate_range(start=initial_date,end=yest_day)
next_days_calendar=pd.bdate_range(start=cur_date,end=final_date)
if next_days_calendar[0]!=cur_date:
    final_date=final_date+BDay(1)
    next_days_calendar=pd.bdate_range(start=cur_date,end=final_date)
last_window=log_returns.tail(5)
print(last_window)
print(last_window_calendar)
last_window.index = last_window_calendar
exog.index =next_days_calendar
df.index =next_days_calendar
last_window=last_window.iloc[:,0]
df['ForecastDate']=cur_date.strftime('%Y-%m-%d')
df.to_csv(home+r"\ResultFiles\Back_Test_Stocks.csv", mode='a', header=False, index=True)
print("ok antes de modelo")
pred = pd.DataFrame(modelo.predict_interval(exog=exog,steps=steps,last_window=last_window))

pred = pred.reset_index().iloc[:,1:]

pred_final = pd.DataFrame(0, index=pred.index, columns=columnas_scaler)
pred_final['GSPC.ReturnSuavizado'] = pred['pred']
#Matriz para intervalo inferior
predlow_final = pd.DataFrame(0, index=pred.index, columns=columnas_scaler)
predlow_final['GSPC.ReturnSuavizado'] = pred['lower_bound']
#Matriz para intervalo superior
predup_final = pd.DataFrame(0, index=pred.index, columns=columnas_scaler)
predup_final['GSPC.ReturnSuavizado'] = pred['upper_bound']


#Transformamos los datos a la representación original.
pred_return = pd.DataFrame(scaler.inverse_transform(pred_final, copy=None))[0]
predlow_return  = pd.DataFrame(scaler.inverse_transform(predlow_final, copy=None))[0]
predup_return  = pd.DataFrame(scaler.inverse_transform(predup_final, copy=None))[0]

#Construimos un dataframe con las predicciones en la representación original
pred = pd.concat([pred_return,predlow_return ,predup_return],axis=1)
pred.columns = ["pred","lower_bound","upper_bound"]
pred.index=pd.bdate_range(start=cur_date,end=final_date)
pred['ForecastDate']=cur_date.strftime('%Y-%m-%d')

pred.to_csv(home+r"\ResultFiles\Back_Test.csv", mode='a', header=False, index=True)
print("ok antes de betas")
cur_date=date.today()
ini_date_beta=cur_date-BDay(20)
acciones=["^GSPC","AAPL","AMZN","MSFT","TSLA","GOOG","GOOGL","NVDA","BRK-B","META","UNH","JNJ","PG"]
acciones = yfin.download(acciones, start=ini_date_beta, end=cur_date)["Adj Close"]

###Calcular los retornos logaritmicos
log_returns_acciones=(np.log(1+acciones.pct_change()))*100
log_returns_acciones.tail()

##Se elimina la primera fila
log_returns_acciones=log_returns_acciones.dropna()

X=log_returns_acciones.iloc[:,12]
X= sm.add_constant(X, prepend=True)
modelo = sm.OLS(endog=log_returns_acciones.iloc[:,1], exog=X)
modelo = modelo.fit()
# print(modelo.summary())
###Valores de alpha, valor p alpha , beta, valor p beta

Accion=[]
Alpha=[]
ValorPAlpha=[]
Beta=[]
ValorPBeta=[]

for i in range(0,(len(log_returns_acciones.columns)-1)):
    X=log_returns_acciones.iloc[:,12]
    X= sm.add_constant(X, prepend=True)
    modelo = sm.OLS(endog=log_returns_acciones.iloc[:,i], exog=X)
    modelo = modelo.fit()
    
    Accion.append(log_returns_acciones.columns[i])
    Alpha.append(round(modelo.params[0],3))
    Beta.append(round(modelo.params[1],3))
    ValorPAlpha.append(round(modelo.pvalues[0],3))
    ValorPBeta.append(round(modelo.pvalues[1],3))  

result = list(zip(Accion,Alpha, ValorPAlpha, Beta,ValorPBeta))
betas = pd.DataFrame(result)
betas = betas.rename(columns={0:'Accion',1:'Alpha',2:'Valor-p Alpha',3:'Beta',4:'Valor-p Beta' })


pred['Stock']='S&P500'

New_Stocks=[]
for i in range(betas.shape[0]):
    for j in range(pred.shape[0]):
        new_line=[]
        beta_temp=betas.Beta.iloc[i]
        stock_temp=betas.Accion.iloc[i]
        new_line.append(pred.index[j])
        new_line.append(pred.pred[j]*betas.Beta[i])
        new_line.append(pred.lower_bound[j]*betas.Beta[i])
        new_line.append(pred.upper_bound[j]*betas.Beta[i])
        new_line.append(stock_temp)
        New_Stocks.append(new_line)

New_Stocks=pd.DataFrame(New_Stocks, columns=['Date','pred','lower_bound','upper_bound','Stock'])
New_Stocks.set_index('Date',inplace=True)

log_returns_acciones=log_returns_acciones[log_returns_acciones.index>=min(log_returns.index)]

log_returns_acciones.to_csv(home+r"\ResultFiles\historico_acciones.csv",index=True)
New_Stocks.to_csv(home+r"\ResultFiles\futuro_acciones.csv",index=True)
betas.to_csv(home+r"\ResultFiles\betas.csv",index=True)
acciones.to_csv(home+r"\ResultFiles\precio_acciones.csv",index=True)