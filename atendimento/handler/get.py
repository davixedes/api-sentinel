import json
from .db import get_atendimento

def handler(event, context):
    path = event.get("pathParameters") or {}
    try:
        func_id = int(path["funcId"])
        ocorr_id = int(path["ocorrId"])
    except (KeyError, ValueError):
        return {"statusCode": 400, "body": json.dumps({"error": "IDs inválidos"})}

    try:
        rec = get_atendimento(func_id, ocorr_id)
        if rec is None:
            return {"statusCode": 404, "body": json.dumps({"error": "Não encontrado"})}
        return {"statusCode": 200, "body": json.dumps(rec, default=str)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
