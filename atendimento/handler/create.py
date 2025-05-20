import json
from .db import create_atendimento

def handler(event, context):
    payload = json.loads(event.get('body', '{}'))
    try:
        create_atendimento(payload)
        return {"statusCode": 201, "body": json.dumps({"message": "Atendimento criado"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
