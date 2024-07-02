import pandas as pd
import logging
import psycopg2
import json

from sqlalchemy import create_engine
from datetime import timedelta,datetime

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s ::DataConnectionModule-> %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
    
def get_conn(**kwargs):
    print(f"Conectandose a la BD en la fecha: {kwargs["exec_date"]}") 
    try:
        conn = psycopg2.connect(
            host = kwargs["config"]["host"],
            dbname = kwargs["config"]["database"],
            user = kwargs["config"]["username"],
            password = kwargs["config"]["pwd"],
            port = kwargs["config"]["port"])
        print(conn)
        print("Connected to Redshift successfully!")
        #logging.info("Connected to Redshift successfully!")
    except Exception as e:
        print("Unable to connect to Redshift.")
        print(e)
        #logging.error("Unable to connect to Redshift. ", e)
    #engine = create_engine(f'redshift+psycopg2://{redshift_conn["username"]}:{redshift_conn["pwd"]}@{redshift_conn["host"]}:{redshift_conn["port"]}/{redshift_conn["database"]}')
    #print(engine)
    

def upload_data(**kwargs):

    print(f"Cargando la data para la fecha: {kwargs["exec_date"]}")
    date = datetime.strptime(kwargs["exec_date"], '%Y-%m-%d %H')

    path = kwargs["dag_path"]+'/raw_data/'+"data_"+str(date.year)+'-'+str(date.month)+'-'+str(date.day)+'-'+str(date.hour)+".json"
    #print(path)

    with open(path, "r") as json_file:
        loaded_data=json.load(json_file)
    # Extraer la data en tabla
    #datax = loaded_data['data']
    records = pd.json_normalize(loaded_data)

    #records=pd.read_csv(path,sep=",")
    #print(records.head())

    #conn = psycopg2.connect(
    #    host = kwargs["config"]["host"],
    #    dbname = kwargs["config"]["database"],
    #    user = kwargs["config"]["username"],
    #    password = kwargs["config"]["pwd"],
    #    port = kwargs["config"]["port"])
    
    host = kwargs["config"]["host"]
    dbname = kwargs["config"]["database"]
    username = kwargs["config"]["username"]
    password = kwargs["config"]["pwd"]
    port = kwargs["config"]["port"]
    
    connection_url = f"redshift+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
    db_engine = create_engine(connection_url)
    
    try:
        records.to_sql(
            kwargs["table"],
            con=db_engine,
            schema=kwargs["schema"],
            if_exists='replace',
            index=False
        )

        #logging.info(f"Data from the DataFrame has been uploaded to the {kwargs["schema"]}.{kwargs["table"]} table in Redshift.")
        print(f"Data from the DataFrame has been uploaded to the {kwargs["schema"]}.{kwargs["table"]} table in Redshift.")
    except Exception as e:
        #logging.error(f"Failed to upload data to {kwargs["schema"]}.{kwargs["table"]}:\n{e}")
        print(f"Failed to upload data to {kwargs["schema"]}.{kwargs["table"]}:\n{e}")
        raise
    finally:
        if db_engine:
            db_engine.dispose()
            logging.info("Connection to Redshift closed.")
        else:
            logging.warning("No active connection to close.")

def close_conn(self):
    if self.db_engine:
        self.db_engine.dispose()
        logging.info("Connection to Redshift closed.")
    else:
        logging.warning("No active connection to close.")


