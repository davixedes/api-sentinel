# handler_update.py
import json
from .db import update_ocorrencia

def handler(event, context):
    try:
        # 1) valida path parameter
        if 'pathParameters' not in event or 'id' not in event['pathParameters']:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Parâmetro 'id' não fornecido"})
            }
        try:
            occ_id = int(event['pathParameters']['id'])
        except ValueError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "ID inválido, deve ser inteiro"})
            }

        # 2) parse body
        body = json.loads(event.get('body') or "{}")

        # 3) chama a camada de DB
        rows = update_ocorrencia(occ_id, body)

        # 4) se nada foi atualizado, 404
        if rows == 0:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Ocorrência não encontrada"})
            }

        # 5) sucesso sem conteúdo
        return {"statusCode": 204, "body": ""}

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
