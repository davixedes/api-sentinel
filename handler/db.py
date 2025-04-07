import os
import oracledb

# Thick mode: o layer monta as libs em /opt/instantclient_19_10
oracledb.init_oracle_client(lib_dir="/opt/instantclient_19_10")

_connection = None

def get_conn():
    global _connection
    if _connection is None or _connection.closed:
        _connection = oracledb.connect(
            user     = os.environ['ORACLE_USER'],
            password = os.environ['ORACLE_PASSWORD'],
            dsn      = os.environ['ORACLE_DSN']
        )
    return _connection
