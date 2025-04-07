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
        body = json.loads(event['body'])

        sql = """
          UPDATE ocorrencia
             SET tipo_ocorrencia       = :1,
                 data_inicio           = TO_TIMESTAMP(:2, 'YYYY-MM-DD"T"HH24:MI:SS'),
                 data_fim              = CASE WHEN :3 IS NULL THEN NULL ELSE TO_TIMESTAMP(:3, 'YYYY-MM-DD"T"HH24:MI:SS') END,
                 severidade_ocorrencia = :4,
                 fk_estacao_id_estacao = :5,
                 fk_cco_id_cco         = :6,
                 status_ocorrencia     = :7
           WHERE id_ocorrencia = :8
        """

        params = (
            body.get('tipo_ocorrencia'),
            body.get('data_inicio'),
            body.get('data_fim'),
            body.get('data_fim'),  # Repetido devido ao CASE
            body.get('severidade_ocorrencia'),
            body.get('id_estacao'),
            body.get('id_cco'),
            body.get('status_ocorrencia'),
            occ_id
        )

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql, params)
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
