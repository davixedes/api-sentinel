import oracledb
import os

def get_conn():
    try:
        connection = oracledb.connect(
            user=os.environ['ORACLE_USER'],
            password=os.environ['ORACLE_PASSWORD'],
            dsn=os.environ['ORACLE_DSN']
        )
        print("Conexão realizada com sucesso!")
        return connection
    except oracledb.Error as e:
        print("Erro ao conectar:", e)
        raise e
