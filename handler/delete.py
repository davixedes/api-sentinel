import json
from .db import get_conn

def handler(event, context):
    try:
        if 'pathParameters' not in event or 'id' not in event['pathParameters']:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Parâmetro 'id' não fornecido"})
            }
        
        occ_id = event['pathParameters']['id']
        
        conn = get_conn()
        cur = conn.cursor()
        sql = "DELETE FROM ocorrencia WHERE id_ocorrencia = :1"
        cur.execute(sql, (occ_id,))
        conn.commit()
        
        if cur.rowcount == 0:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Ocorrência não encontrada"})
            }
        
        return {"statusCode": 204, "body": ""}
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
