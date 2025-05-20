import json
from .db import update_atendimento

def handler(event, context):
    path = event.get("pathParameters") or {}
    try:
        func_id = int(path["funcId"])
        ocorr_id = int(path["ocorrId"])
        payload = json.loads(event.get('body', '{}'))
    except (KeyError, ValueError):
        return {"statusCode": 400, "body": json.dumps({"error": "Dados de rota ou payload inválidos"})}

    try:
        count = update_atendimento(func_id, ocorr_id, payload)
        if count == 0:
            return {"statusCode": 404, "body": json.dumps({"error": "Não encontrado"})}
        return {"statusCode": 200, "body": json.dumps({"updated": count})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
