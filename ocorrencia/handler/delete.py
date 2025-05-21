import json
from .db import delete_ocorrencia

def handler(event, context):
    try:
        occ_id = int(event["pathParameters"]["id"])
        removed = delete_ocorrencia(occ_id)
        if removed == 0:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Ocorrência não encontrada"})
            }
        # 204 No Content
        return {
            "statusCode": 204,
            "body": ""
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
