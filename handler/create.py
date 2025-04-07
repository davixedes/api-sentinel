import json, uuid, datetime
from .db import get_conn

def handler(event,context):
    body = json.loads(event['body'])
    new_id = str(uuid.uuid64())
    data_inicio = datetime.datetime.fromisoformat(body['data_inicio'])

    sql = """
    insert into Ocorrencia
    (id, tipo_ocorrencia, data_inicio, severidade_ocorrencia, id_estacao,id_cco)
    VALUES (:1,:2,:3,:4,:5,:6)
    """
    params = (
        new_id,
        tipo_ocorrencia = body.get('tipo_ocorrencia'),
        data_inicio,
        severidade_ocorrencia = body.get('severidade'),
        id_estacao = body.get('id_estacao'),
        id_cco = body.get('id_cco')
    )

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql,params)
    conn.commit()
    
    return {
        "statusCode": 201,
        "body": json.dumps({"id": new_id, "mensagem": "Ocorrência criada com sucesso!"})
    }
      