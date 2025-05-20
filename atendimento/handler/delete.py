import json
from ..db import delete_atendimento

def handler(event, context):
    path = event.get("pathParameters") or {}
    try:
        func_id = int(path["funcId"])
        ocorr_id = int(path["ocorrId"])
    except (KeyError, ValueError):
        return {"statusCode": 400, "body": json.dumps({"error": "IDs inválidos"})}

    try:
        count = delete_atendimento(func_id, ocorr_id)
        if count == 0:
            return {"statusCode": 404, "body": json.dumps({"error": "Não encontrado"})}
        return {"statusCode": 200, "body": json.dumps({"deleted": count})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
