import pandas as pd
import urllib.request
import logging
import json

# Se configura el archivo app.log con el formato del mensaje de salida
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

# Se crea la clase DataManager
class DataManager:
    
    # Se crea el metodo get_data para el llamado a la API
    def get_data(self):
        try:
            # Se hace el request a la API
            response = urllib.request.urlopen("https://coronavirus.m.pipedream.net/").read()
            # Se convierte la respuesta en un json
            data = json.loads(response)
            # Se carga para crear un DataFrame obteniendo rawData, que tiene la informacion necesario
            pd_data = pd.json_normalize(data["rawData"])
            return pd_data
        except Exception as e:
            logging.error(e)
        finally:
            logging.warn("Check the data format")

