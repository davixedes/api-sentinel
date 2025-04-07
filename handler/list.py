import json
from .db import get_conn

def handler(event, context):
    # 1) Pega o ID da ocorrência via path parameter
    occ_id = event['pathParameters']['id']
    
    # 2) Faz o parse do JSON enviado no body
    body = json.loads(event['body'])
    
    # 3) Monta o SQL de UPDATE, com placeholders
    sql = """
      UPDATE ocorrencia
         SET tipo_ocorrencia      = :1,
             data_inicio          = TO_TIMESTAMP(:2, 'YYYY-MM-DD"T"HH24:MI:SS'),
             data_fim             = CASE WHEN :3 IS NULL THEN NULL
                                         ELSE TO_TIMESTAMP(:3, 'YYYY-MM-DD"T"HH24:MI:SS')
                                    END,
             severidade_ocorrencia = :4,
             id_estacao           = :5,
             id_cco               = :6
       WHERE id = :7
    """
    
    # 4) Prepara os parâmetros na ordem certa
    params = (
        body.get('tipo_ocorrencia'),
        body.get('data_inicio'),           # ex: "2025-04-06T09:00:00"
        body.get('data_fim'),              # pode ser None
        body.get('severidade_ocorrencia'),
        body.get('id_estacao'),
        body.get('id_cco'),
        occ_id
    )
    
    # 5) Executa o UPDATE e dá commit
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    
    # 6) Opcional: verificar se alguma linha foi afetada
    if cur.rowcount == 0:
        # nenhum registro com esse ID
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Ocorrência não encontrada"})
        }
    
    # 7) Retorna 204 No Content (não precisa enviar body)
    return {
        "statusCode": 204,
        "body": ""
    }
