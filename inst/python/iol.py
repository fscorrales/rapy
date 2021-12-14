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
  response = requests.post(BASE_URL + "/token", headers = h, data = body)
  if response.status_code == 200:
    response = (response.json())
    return response
  else:
    return (f"Error: {response.status_code} con respuesta = {response.text}")
  
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

def iol_seconds_to_expire(iol_response):
  iol_expire = iol_response[".expires"][5::].split(" ")
  iol_expire[1] = LIST_MONTH[iol_expire[1]]
  expire_datetime = " "
  expire_datetime = expire_datetime.join(iol_expire)
  expire_datetime = dt.datetime.strptime(expire_datetime, "%d %m %Y %H:%M:%S %Z")
  sec_to_expire = (expire_datetime - dt.datetime.now()).total_seconds()
  return sec_to_expire

##MI CUENTA
###Estado de Cuenta
def iol_get_estado_de_cuenta(iol_response):
  h = {
    "Authorization":"Bearer " + iol_response["access_token"]
  }
  response = requests.get(BASE_URL + "/api/v2/estadocuenta", headers = h)
  if response.status_code == 200:
    response = response.json()
    response = response["cuentas"]
    response = pd.json_normalize(
    response, "saldos", ["numero", "tipo", "moneda", "titulosValorizados",
    "total", "margenDescubierto"]
    )
    response.columns = ["liquidacion", "saldo", "comprometido", "disponible",
    "disponible_operar", "nro_cta", "tipo", "moneda", "titulos_valorizados",
    "total", "margen_descubierto"]  
    return response
  else:
    return (f"Error: {response.status_code} con respuesta = {response.text}")
  
###Portafolio (Verificar que pasa cuando hay varias operaciones en distintos plazos)
def iol_get_portafolio(iol_response, pais = "argentina"):
  h = {
    "Authorization":"Bearer " + iol_response["access_token"]
  }
  endpoint = BASE_URL + f"/api/v2/portafolio/{pais}"
  response = requests.get(endpoint, headers = h)
  if response.status_code == 200:
    response = (response.json())
    response = response["activos"]
    response = pd.json_normalize(response)
    return response
  else:
    return (f"Error: {response.status_code} con respuesta = {response.text}")
  
###Operación
def iol_get_operacion(iol_response, numero):
  h = {
    "Authorization":"Bearer " + iol_response["access_token"]
  }
  endpoint = BASE_URL + f"/api/v2/operaciones/{numero}"
  response = requests.get(endpoint, headers = h)
  if response.status_code == 200:
    response = (response.json())
    response = pd.DataFrame(response)
    return response
  else:
    return (f"Error: {response.status_code} con respuesta = {response.text}")
  
###Delete operación
def iol_delete_operacion(iol_response, numero):
  h = {
    "Authorization":"Bearer " + iol_response["access_token"]
  }
  endpoint = BASE_URL + f"/api/v2/operaciones/{numero}"
  response = requests.delete(endpoint, headers = h)
  if response.status_code == 200:
    response = (response.json())
    response = pd.DataFrame(response)
    return response
  else:
    return (f"Error: {response.status_code} con respuesta = {response.text}")


###Operaciones
def iol_get_operaciones(iol_response, numero = "", estado = "",
fecha_desde  = "", fecha_hasta = "", pais = ""):
  h = {
    "Authorization":"Bearer " + iol_response["access_token"]
  }
  if numero != "":
    he = {
      "filtro.numero":numero
    }
    h = {**h, **he}
  if estado != "":
    he = {
      "filtro.estado":estado
    }
    h = {**h, **he}  
  if fecha_desde != "":
    he = {
      "filtro.fechaDesde":fecha_desde
    }
    h = {**h, **he} 
  if fecha_hasta != "":
    he = {
      "filtro.fechaHasta":fecha_hasta
    }
    h = {**h, **he} 
  if pais != "":
    he = {
      "filtro.pais":pais
    }
    h = {**h, **he}
  endpoint = BASE_URL + f"/api/v2/operaciones"
  response = requests.get(endpoint, headers = h)
  if response.status_code == 200:
    response = (response.json())
    response = pd.DataFrame(response)
    return response
  else:
    return (f"Error: {response.status_code} con respuesta = {response.text}")
  
###Get Resumen Cuenta Remunerada (not working?)
def iol_get_resumen_cuenta_remunerada(iol_response):
  h = {
    "Authorization":"Bearer " + iol_response["access_token"]
  }
  endpoint = BASE_URL + f"/api/v2/GetResumenCuentaRemunerada"
  response = requests.get(endpoint, headers = h)
  if response.status_code == 200:
    response = pd.DataFrame(response.json())
    return response
  else:
    return (f"Error: {response.status_code} con respuesta = {response.text}")
  
##TITULOS
###Instrumentos por país
def iol_get_instrumentos_por_pais(iol_response, pais = "argentina"):
  h = {
    "Authorization":"Bearer " + iol_response["access_token"]
  }
  endpoint = BASE_URL + f"/api/v2/{pais}/Titulos/Cotizacion/Instrumentos"
  response = requests.get(endpoint, headers = h)
  if response.status_code == 200:
    response = (response.json())
    response = pd.DataFrame(response)
    return response
  else:
    return (f"Error: {response.status_code} con respuesta = {response.text}")


###Get Cotizacion Historica por simbolo
def iol_get_cotizacion_historica_simbolo(iol_response, simbolo, 
mercado = "bCBA", fecha_desde = "2010-01-01", fecha_hasta = "",
ajustada = "ajustada"):
  h = {
    "Authorization":"Bearer " + iol_response["access_token"]
  }
  if (fecha_hasta == ""):
    fecha_hasta = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d")
  endpoint = BASE_URL + f"/api/v2/{mercado}/Titulos/{simbolo}/Cotizacion/seriehistorica/{fecha_desde}/{fecha_hasta}/{ajustada}"
  response = requests.get(endpoint, headers = h)
  if response.status_code == 200:
    response = (response.json())
    response = pd.DataFrame(response)
    response.columns = ["close", "var", "open", "high", "low", "fecha_hora",
    "tendencia", "previous_close", "monto_operado", "volumen_nominal",
    "precio_promedio", "moneda", "precio_ajuste", "open_interest",
    "puntas", "q_operaciones"]
    return response
  else:
    return (f"Error: {response.status_code} con respuesta = {response.text}")


 # response["fecha_hora"] = response["fecha_hora"].apply(lambda x: x[0:10])
  # y["fecha_hora"] = pd.to_datetime(y["fecha_hora"])
  # y["fecha_hora"] = y["fecha_hora"].date()
  
