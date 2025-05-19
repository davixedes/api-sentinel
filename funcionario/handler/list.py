import json
from .db import list_funcionarios

def handler(event, context):
    try:
        funcionarios = list_funcionarios()
        return {
            "statusCode": 200,
            "body": json.dumps(funcionarios, default=str)
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
