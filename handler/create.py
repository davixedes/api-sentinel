import json
from .db import create_ocorrencia

def handler(event, context):
    try:
        body = json.loads(event.get('body') or "{}")

        # validações mínimas
        required = ['tipo_ocorrencia', 'data_inicio', 'severidade_ocorrencia', 'id_estacao', 'id_cco']
        for key in required:
            if key not in body:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Campo obrigatório '{key}' não fornecido"})
                }

        new_id = create_ocorrencia(body)

        return {
            "statusCode": 201,
            "body": json.dumps({"id_ocorrencia": new_id})
        }

    except ValueError as ve:
        # falha em conversão de tipo
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(ve)})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
