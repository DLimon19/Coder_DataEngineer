from datetime import timedelta,datetime

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

# Se crea el metodo get_data para el llamado a la API
def get_data(**kwargs):
    try:
        print(f"Adquiriendo data para la fecha: {kwargs["exec_date"]}")
        date = datetime.strptime(kwargs["exec_date"], '%Y-%m-%d %H')
        # Se hace el request a la API
        response = urllib.request.urlopen("https://coronavirus.m.pipedream.net/").read()
        if response:
            print('Llamada a la API exitosa!')
            #logging.info("Success")
            # Se convierte la respuesta en un json
            data = json.loads(response)
            # Se carga para crear un DataFrame obteniendo rawData, que tiene la informacion necesario
            #pd_data = pd.json_normalize(data["rawData"])
            #return pd_data

            with open(kwargs["dag_path"]+'/raw_data/'+"data_"+str(date.year)+'-'+str(date.month)+'-'+str(date.day)+'-'+str(date.hour)+".json", "w") as json_file:
                   json.dump(data["rawData"], json_file)

            # Se crea archivo csv
            #pd_data.to_csv(kwargs["dag_path"]+'/raw_data/'+"data_"+str(date.year)+'-'+str(date.month)+'-'+str(date.day)+'-'+str(date.hour)+".csv", index=False, mode='a',header=False)
        else:
            print('An error has occured!')
            #logging.info('An error has occured!')
    except Exception as e:
        #logging.error(e)
        print(e)
    finally:
        #logging.warn("Check the data format")
        print("Check the data format")

