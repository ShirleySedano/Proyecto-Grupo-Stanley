####GARH MSFT

MSFT<-function(){
  ##Librerias
  
  library(quantmod)
  library(ggplot2)
  library(dygraphs)
  library(dplyr)
  library(xts)
  library(ggcorrplot)
  library(tidyverse)
  library(lubridate)
  library(tseries)
  library(tsoutliers)
  library(tsbox)
  library(forecast)
  library(data.table)
  library(ggcorrplot)
  library(TSstudio)
  library(fImport)
  library(vars)
  library(rugarch)
  library(readr)
  delay <- read_csv("C:/Users/aparra/Desktop/EntregaFinalMaestria/MSFTStock/delay.csv")
  
  
  
  inicio="2012-05-18"
  fin=Sys.Date()-delay$delay
  inicio=Sys.Date()-delay$delay-150
  nombreAcciones<-c("MSFT")
  acciones<-getSymbols(nombreAcciones, src = "yahoo", from =inicio, to = fin, periodicity = "daily")
  CierreAjustado<- cbind(MSFT$MSFT.Adjusted)
  
  ###Calcular retornos diarios
  Rendimientos<-(periodReturn(CierreAjustado$MSFT.Adjusted, period = "daily",type="log")*100)
  
  ###Model Garch
  ugarch1 = ugarchspec(mean.model = list(armaOrder = c(0,1),include.mean = TRUE),variance.model = list(garchOrder=c(1,1)))
  ugfit = ugarchfit(spec = ugarch1, data = Rendimientos)
  
  ###Simulacion
  
  garch11.sim = ugarchsim(ugfit, n.sim=7 , m.sim=1, startMethod="sample")
  simulacion<-data.frame(garch11.sim@simulation$seriesSim)
  simulacion1<-apply(simulacion, 1, mean)
  simulacion1<-data.frame(simulacion=simulacion1)
  return(simulacion1)
  
}

MSFT()
