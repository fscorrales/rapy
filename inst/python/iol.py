# pip install pandas
import pandas as pd

#Importamos Panel Lider (web scraping)
def iol_scraping_panel_lider():
  df = pd.read_html(
    "https://iol.invertironline.com/Mercado/Cotizaciones",
    decimal=',', thousands='.')
  df = df[0]
  df.rename(columns = {"Símbolo":"simbolo", "ÚltimoOperado":"ultimo_operado",
  "VariaciónDiaria":"var_diaria", "CantidadCompra":"cantidad_compra",
  "PrecioCompra":"precio_compra", "PrecioVenta":"precio_venta", 
  "CantidadVenta":"cantidad_venta", "Apertura":"open", 
  "Mínimo":"min", "Máximo":"max", "ÚltimoCierre":"close", 
  "MontoOperado":"monto", "Fecha/Hora":"fecha"}, inplace = True)
  df.simbolo = df.simbolo.str.split(" ")
  df.simbolo = df.simbolo.apply(lambda x: x[0])
  return df

iol_scraping_panel_lider()
