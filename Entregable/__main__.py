import os
import logging

from modules import DataManager
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

# Se obtienen las credenciales de redshift del archivo .env
username = os.getenv('REDSHIFT_USERNAME')
password = os.getenv('REDSHIFT_PASSWORD')
host = os.getenv('REDSHIFT_HOST')
port = os.getenv('REDSHIFT_PORT', '5439')
dbname = os.getenv('REDSHIFT_DBNAME')

# se asignan variables con el schema y la tabla de la base de datos
schema = "luis_981908_coderhouse"
table = "stage_covid_data"

# se crea la conexion a redshift
connection_url = f"redshift+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
db_engine = create_engine(connection_url)

try:
    db_engine.connect()
    logging.info("Connection created")
except Exception as e:
    logging.error(f"Failed to create connection: {e}")
    raise

# Se manda a llamar get_data() que hace el request a la API y regresa un DataFrame
try:
    data = DataManager().get_data()

    # Se manda la informacion desde el DataFrame con la data a la base de datos
    data.to_sql(
        table,
        con=db_engine,
        schema=schema,
        if_exists='append',
        index=False
    )

    logging.info(f"Data from the DataFrame has been uploaded to the {schema}.{table} table in Redshift.")
        
except Exception as e:
    logging.error(f"Failed to upload data to {schema}.{table}: {e}")
    raise
finally:
    # Si la conexion existe, se cierra
    if db_engine:
        db_engine.dispose()
        logging.info("Connection to Redshift closed.")
    else:
        logging.warning("No active connection to close.")