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

##TIME TO EXPIRE
LIST_MONTH = {
  "Jan":"01",
  "Feb":"02",
  "Mar":"03",
  "Apr":"04",
  "May":"05",
  "Jun":"06",
  "Jul":"07",
  "Aug":"08",
  "Sep":"09",
  "Oct":"10",
  "Nov":"11",
  "Dec":"12"
}

def iol_seconds_to_expire(iol_response = 0):
  iol_expire = iol_response[".expires"][5::].split(" ")
  iol_expire[1] = LIST_MONTH[iol_expire[1]]
  expire_datetime = " "
  expire_datetime = expire_datetime.join(iol_expire)
  expire_datetime = dt.datetime.strptime(expire_datetime, "%d %m %Y %H:%M:%S %Z")
  sec_to_expire = (expire_datetime - dt.datetime.now()).total_seconds()
  return sec_to_expire

##MI CUENTA
###Estado de Cuenta
def iol_estado_de_cuenta(iol_response):
  h = {
    "Authorization":"Bearer " + iol_response["access_token"]
  }
  response = requests.get(BASE_URL + "/api/v2/estadocuenta", headers = h).json()
  response = response["cuentas"]
  response = pd.json_normalize(
    response, "saldos", ["numero", "tipo", "moneda", "titulosValorizados",
    "total", "margenDescubierto"]
    )
  response.columns = ["liquidacion", "saldo", "comprometido", "disponible",
  "disponible_operar", "nro_cta", "tipo", "moneda", "titulos_valorizados",
  "total", "margen_descubierto"]  
  return response
