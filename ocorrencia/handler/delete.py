import json
from .db import delete_ocorrencia

def handler(event, context):
    try:
        # Valida presença do path parameter 'id'
        if 'pathParameters' not in event or 'id' not in event['pathParameters']:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Parâmetro 'id' não fornecido"})
            }

        # Converte para inteiro
        try:
            occ_id = int(event['pathParameters']['id'])
        except ValueError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "ID inválido, deve ser inteiro"})
            }

        # Chama a rotina de delete
        deleted = delete_ocorrencia(occ_id)

        if deleted == 0:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Ocorrência não encontrada"})
            }

        # 204 No Content
        return {"statusCode": 204, "body": ""}

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
