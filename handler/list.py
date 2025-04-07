import json
from .db import get_conn

def handler(event, context):
    try:
        sql = "SELECT * FROM ocorrencia"
        
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        
        ocorrencias = [dict(zip(columns, row)) for row in rows]
        
        return {
            "statusCode": 200,
            "body": json.dumps(ocorrencias, default=str)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
