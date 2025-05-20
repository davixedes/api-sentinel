import json
from .db import list_atendimentos

def handler(event, context):
    try:
        items = list_atendimentos()
        return {"statusCode": 200, "body": json.dumps(items, default=str)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
