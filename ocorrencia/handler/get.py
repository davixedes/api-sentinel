# ocorrencia/handler/get.py

import json
from .db import get_ocorrencia

def handler(event, context):
    try:
        occ_id = int(event["pathParameters"]["id"])
        rec = get_ocorrencia(occ_id)
        if rec:
            return {"statusCode":200, "body": json.dumps(rec)}
        else:
            return {"statusCode":404, "body": json.dumps({"error":"Não encontrado"})}
    except Exception as e:
        return {"statusCode":500, "body": json.dumps({"error": str(e)})}
