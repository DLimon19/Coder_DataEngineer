import os

from modules import DataConn, DataManager
from dotenv import load_dotenv



load_dotenv()

user_credentials = {
    "REDSHIFT_USERNAME" : os.getenv('REDSHIFT_USERNAME'),
    "REDSHIFT_PASSWORD" : os.getenv('REDSHIFT_PASSWORD'),
    "REDSHIFT_HOST" : os.getenv('REDSHIFT_HOST'),
    "REDSHIFT_PORT" : os.getenv('REDSHIFT_PORT', '5439'),
    "REDSHIFT_DBNAME" : os.getenv('REDSHIFT_DBNAME')
}

schema = "luis_981908_coderhouse"
data_conn = DataConn(user_credentials, schema)

try:
    data_conn.get_conn()
    data = DataManager().get_data()
    data_conn.upload_data(data, "stage_covid_data")
finally:
    data_conn.close_conn()