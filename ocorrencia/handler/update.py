# ocorrencia/handler/update.py

import json
from .db import update_ocorrencia

def handler(event, context):
    try:
        occ_id = int(event["pathParameters"]["id"])
        payload = json.loads(event["body"])
        updated = update_ocorrencia(occ_id, payload)
        if updated:
            # 204 No Content
            return {"statusCode": 204, "body": ""}
        else:
            return {"statusCode": 404, "body": json.dumps({"error":"Não encontrado"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
