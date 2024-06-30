from sqlalchemy import create_engine
import logging
from modules import DataConn

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s ::DataConnectionModule-> %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

def executeSqlFromFile(filename, conn: DataConn):

    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')
    if conn.db_engine is None:
        logging.warn("Execute it before")
        conn.get_conn()

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        if command == '':
            continue
        
        try:
            conn.db_engine.execute(command)
        except Exception as e:
            logging.error(f"Failed to excecute sql command: {e}")
            raise