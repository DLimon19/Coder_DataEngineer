import os
import logging
import pandas as pd

from modules import DataManager, DataConn, executeSqlFromFile
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Se configura el archivo app.log con el formato del mensaje de salida
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

# Se cargan las dependencias del venv
load_dotenv()

def main():
    # Se obtienen las credenciales de redshift del archivo .env
    user_credentials = {
        "REDSHIFT_USERNAME" : os.getenv('REDSHIFT_USERNAME'),
        "REDSHIFT_PASSWORD" : os.getenv('REDSHIFT_PASSWORD'),
        "REDSHIFT_HOST" : os.getenv('REDSHIFT_HOST'),
        "REDSHIFT_PORT" : os.getenv('REDSHIFT_PORT', '5439'),
        "REDSHIFT_DBNAME" : os.getenv('REDSHIFT_DBNAME')
    }

    # se asignan variables con el schema y la tabla de la base de datos
    schema = "luis_981908_coderhouse"
    table = "stage_covid_data"
    view = "covid_data_analist"

    # se crea la conexion a redshift y el objeto tipo data manager
    data_conn = DataConn(user_credentials,schema)
    data_man = DataManager()

    try:
        executeSqlFromFile('sql_data.sql', data_conn)
    finally:
        data_conn.close_conn()

    try:
        # Se hace el request a la API y se carga la informacion a la base de datos de redshift
        data = data_man.get_data()
        data_conn.upload_data(data, table)            
    except Exception as e:
        logging.error(f"Failed to upload data to {schema}.{table}: {e}")
    finally:
        data_conn.close_conn()

if __name__ == "__main__" :
    main()