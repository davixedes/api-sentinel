# handler/delete.py
import json
from .db import get_conn

def handler(event, context):
    # 1) Pega o ID da ocorrência dos path parameters
    occ_id = event['pathParameters']['id']
    
    # 2) Conecta e prepara o cursor
    conn = get_conn()
    cur  = conn.cursor()
    
    # 3) Executa o DELETE parametrizado
    sql = "DELETE FROM ocorrencia WHERE id = :1"
    cur.execute(sql, (occ_id,))
    
    # 4) Confirma a transação
    conn.commit()
    
    # 5) Se não deletou nada, retorna 404
    if cur.rowcount == 0:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Ocorrência não encontrada"})
        }
    
    # 6) Sucesso: 204 No Content
    return {
        "statusCode": 204,
        "body": ""
    }
