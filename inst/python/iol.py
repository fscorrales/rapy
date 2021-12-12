#Importamos librerias
import pandas as pd
import datetime as dt
import requests

#Importamos Panel Lider (web scraping)
def iol_scraping_panel_lider():
  df = pd.read_html(
    "https://iol.invertironline.com/Mercado/Cotizaciones",
    decimal=',', thousands='.')
  df = df[0]
  df = df.iloc[:, 0:13]
  df.rename(columns = {"Símbolo":"simbolo", "ÚltimoOperado":"ultimo_operado",
  "VariaciónDiaria":"var_diaria", "CantidadCompra":"cantidad_compra",
  "PrecioCompra":"precio_compra", "PrecioVenta":"precio_venta", 
  "CantidadVenta":"cantidad_venta", "Apertura":"open", 
  "Mínimo":"min", "Máximo":"max", "ÚltimoCierre":"close", 
  "MontoOperado":"monto", "Fecha/Hora":"hora"}, inplace = True)
  df.insert((len(df.columns) - 1), "fecha", str(dt.date.today())) 
  df.simbolo = df.simbolo.str.split(" ")
  df.simbolo = df.simbolo.apply(lambda x: x[0])
  return df

iol_scraping_panel_lider()

#API IOL
BASE_URL = "https://api.invertironline.com"

## AUTENTICACIÓN

"""
https://api.invertironline.com/token
POST /token HTTP/1.1
Host: api.invertironline.com
Content-Type: application/x-www-form-urlencoded
username=MIUSUARIO&password=MICONTRASEÑA&grant_type=password
"""

def iol_authentication(user_name, password):
  h = {
  "Content-Type":"application/x-www-form-urlencoded"
  }
  body = {
    "username":user_name,
    "password":password,
    "grant_type":"password"
  }
  response = requests.post(BASE_URL + "/token", headers = h, data = body).json()
  if 'error' in response.keys():
      print('Error found: ' + response['error'])
  else:
    return response
  
#iol_response = iol_authentication("iol_user_name", "iol_password")
