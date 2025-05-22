import json
from .db import list_ocorrencias

def handler(event, context):
    try:
        items = list_ocorrencias()
        return {
            "statusCode": 200,
            "body": json.dumps(items)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
