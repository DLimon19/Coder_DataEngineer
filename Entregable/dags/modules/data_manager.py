from datetime import datetime

import pandas as pd
import urllib.request
import json

# Se crea el metodo get_data para el llamado a la API
def get_data(**kwargs):
    try:
        print(f"Adquiriendo data para la fecha: {kwargs["exec_date"]}")
        date = datetime.strptime(kwargs["exec_date"], '%Y-%m-%d %H')
        # Se hace el request a la API
        response = urllib.request.urlopen("https://coronavirus.m.pipedream.net/").read()
        if response:
            print('Llamada a la API exitosa!')
            # Se convierte la respuesta en un json
            data = json.loads(response)
            # Se crea un archivo json en el directorio ./raw_data/ y se le cargan los datos
            with open(kwargs["dag_path"]+'/raw_data/'+"data_"+str(date.year)+'-'+str(date.month)+'-'+str(date.day)+'-'+str(date.hour)+".json", "w") as json_file:
                   json.dump(data["rawData"], json_file)
        else:
            print('An error has occured!')
    except Exception as e:
        #logging.error(e)
        print(e)
    finally:
        print("Check the data format")

