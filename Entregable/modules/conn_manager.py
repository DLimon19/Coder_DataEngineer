import pandas as pd
import logging


from sqlalchemy import create_engine

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s ::DataConnectionModule-> %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
    
class DataConn:
    def __init__(self, config: dict,schema: str):
        self.config = config
        self.schema = schema
        self.db_engine = None


    def get_conn(self):
        username = self.config.get('REDSHIFT_USERNAME')
        password = self.config.get('REDSHIFT_PASSWORD')
        host = self.config.get('REDSHIFT_HOST')
        port = self.config.get('REDSHIFT_PORT', '5439')
        dbname = self.config.get('REDSHIFT_DBNAME')

        # Construct the connection URL
        connection_url = f"redshift+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
        self.db_engine = create_engine(connection_url)

        try:
            with self.db_engine.connect() as connection:
                result = connection.execute('SELECT 1;')
            if result:
                logging.info("Connection created")
                return
        except Exception as e:
            logging.error(f"Failed to create connection: {e}")
            raise
    

    def upload_data(self, data: pd.DataFrame, table: str):
        if self.db_engine is None:
            logging.warn("Execute it before")
            self.get_conn()

        try:
            data.to_sql(
                table,
                con=self.db_engine,
                schema=self.schema,
                if_exists='append',
                index=False
            )

            logging.info(f"Data from the DataFrame has been uploaded to the {self.schema}.{table} table in Redshift.")
        except Exception as e:
            logging.error(f"Failed to upload data to {self.schema}.{table}:\n{e}")
            raise

    def close_conn(self):
        if self.db_engine:
            self.db_engine.dispose()
            logging.info("Connection to Redshift closed.")
        else:
            logging.warning("No active connection to close.")


