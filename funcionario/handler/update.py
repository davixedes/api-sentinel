import json
from .db import update_funcionario

def handler(event, context):
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {"statusCode": 400, "body": json.dumps({"error": "ID não fornecido"})}

    func_id = int(event["pathParameters"]["id"])
    try:
        payload = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return {"statusCode": 400, "body": json.dumps({"error": "JSON inválido"})}

    try:
        updated = update_funcionario(func_id, payload)
        if updated == 0:
            return {"statusCode": 404, "body": json.dumps({"error": "Funcionário não encontrado"})}
        return {"statusCode": 204, "body": ""}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
