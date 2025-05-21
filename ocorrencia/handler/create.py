import json
from .db import create_ocorrencia, get_ocorrencia

def handler(event, context):
    try:
        payload = json.loads(event.get("body", "{}"))
        new_id = create_ocorrencia(payload)
        # opcional: buscar o registro completo pra retornar
        record = get_ocorrencia(new_id)
        return {
            "statusCode": 201,
            "body": json.dumps(record)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
