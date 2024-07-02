import pandas as pd
import psycopg2
import json

from sqlalchemy import create_engine
from datetime import datetime
    
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
    except Exception as e:
        print("Unable to connect to Redshift.")
        print(e)

def upload_data(**kwargs):

    print(f"Cargando la data para la fecha: {kwargs["exec_date"]}")
    date = datetime.strptime(kwargs["exec_date"], '%Y-%m-%d %H')

    path = kwargs["dag_path"]+'/raw_data/'+"data_"+str(date.year)+'-'+str(date.month)+'-'+str(date.day)+'-'+str(date.hour)+".json"

    with open(path, "r") as json_file:
        loaded_data=json.load(json_file)
    records = pd.json_normalize(loaded_data)
    
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

        print(f"Data from the DataFrame has been uploaded to the {kwargs["schema"]}.{kwargs["table"]} table in Redshift.")
    except Exception as e:
        print(f"Failed to upload data to {kwargs["schema"]}.{kwargs["table"]}:\n{e}")
        raise
    finally:
        if db_engine:
            db_engine.dispose()
            print("Connection to Redshift closed.")
        else:
            print("No active connection to close.")



