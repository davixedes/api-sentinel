import json
from .db import create_funcionario

def handler(event, context):
    try:
        payload = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return {"statusCode": 400, "body": json.dumps({"error": "JSON inválido"})}

    # Validação mínima
    if not payload.get("nome") or payload.get("status") is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "'nome' e 'status' são obrigatórios"})
        }

    try:
        new_id = create_funcionario(payload)
        return {
            "statusCode": 201,
            "body": json.dumps({"id_funcionario": new_id})
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
