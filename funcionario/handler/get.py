import json
from .db import get_funcionario_by_id

def handler(event, context):
    # Valida se veio o ID na URL
    path = event.get("pathParameters") or {}
    if "id" not in path:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "ID do funcionário não fornecido"})
        }

    try:
        func_id = int(path["id"])
    except ValueError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "ID inválido"})
        }

    try:
        func = get_funcionario_by_id(func_id)
        if func is None:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Funcionário não encontrado"})
            }
        return {
            "statusCode": 200,
            "body": json.dumps(func, default=str)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
