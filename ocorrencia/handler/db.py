# ocorrencia/handler/db.py

import os
import oracledb
from datetime import datetime, date

def get_conn():
    """Retorna uma conexão aberta com o Oracle."""
    try:
        return oracledb.connect(
            user=os.environ['ORACLE_USER'],
            password=os.environ['ORACLE_PASSWORD'],
            dsn=os.environ['ORACLE_DSN']
        )
    except oracledb.Error as e:
        print("Erro ao conectar:", e)
        raise

def _to_iso(val):
    """Converte DATE/TIMESTAMP Oracle para ISO-8601 ou None."""
    if val is None:
        return None
    if isinstance(val, datetime):
        return val.isoformat(timespec="seconds")
    if isinstance(val, date):
        return datetime.combine(val, datetime.min.time()).isoformat(timespec="seconds")
    return str(val)

def create_ocorrencia(payload: dict):
    """
    Insere uma ocorrência e retorna o id gerado pelo IDENTITY.
    Expect: tipo_ocorrencia, data_inicio, data_fim (opt), severidade_ocorrencia,
            id_estacao, id_cco, status_ocorrencia (opt)
    """
    sql = """
    INSERT INTO ocorrencia (
      tipo_ocorrencia,
      data_inicio,
      data_fim,
      severidade_ocorrencia,
      fk_estacao_id_estacao,
      fk_cco_id_cco,
      status_ocorrencia
    ) VALUES (
      :tipo,
      TO_TIMESTAMP(:data_inicio, 'YYYY-MM-DD"T"HH24:MI:SS'),
      CASE WHEN :data_fim IS NULL THEN NULL
           ELSE TO_TIMESTAMP(:data_fim, 'YYYY-MM-DD"T"HH24:MI:SS') END,
      :severidade,
      :id_estacao,
      :id_cco,
      :status
    )
    RETURNING id_ocorrencia INTO :id_out
    """
    conn = get_conn()
    cur = conn.cursor()
    id_out = cur.var(oracledb.DB_TYPE_NUMBER)

    binds = {
        "tipo":       payload["tipo_ocorrencia"],
        "data_inicio":payload["data_inicio"],
        "data_fim":   payload.get("data_fim"),
        "severidade": int(payload["severidade_ocorrencia"]),
        "id_estacao": int(payload["id_estacao"]),
        "id_cco":     int(payload["id_cco"]),
        "status":     payload.get("status_ocorrencia", "ABERTO"),
        "id_out":     id_out,
    }

    cur.execute(sql, binds)
    conn.commit()
    return int(id_out.getvalue()[0])

def get_ocorrencia(occ_id: int):
    """
    Busca uma ocorrência por ID.
    Retorna dict ou None.
    """
    sql = """
    SELECT
      id_ocorrencia,
      data_inicio,
      data_fim,
      tipo_ocorrencia,
      descricao_ocorrencia,
      severidade_ocorrencia,
      fk_estacao_id_estacao AS id_estacao,
      fk_cco_id_cco         AS id_cco,
      status_ocorrencia
    FROM ocorrencia
    WHERE id_ocorrencia = :id
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, {"id": occ_id})
    row = cur.fetchone()
    if not row:
        return None

    cols = [col[0].lower() for col in cur.description]
    rec = dict(zip(cols, row))
    # converte datas para ISO
    rec["data_inicio"] = _to_iso(rec["data_inicio"])
    rec["data_fim"]    = _to_iso(rec["data_fim"])
    return rec

def list_ocorrencias() -> list[dict]:
    """
    Retorna todas as ocorrências como lista de dicts (com datas em ISO).
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ocorrencia")
    rows = cur.fetchall()
    cols = [col[0].lower() for col in cur.description]
    result = []
    for row in rows:
        rec = dict(zip(cols, row))
        rec["data_inicio"] = _to_iso(rec["data_inicio"])
        rec["data_fim"]    = _to_iso(rec["data_fim"])
        result.append(rec)
    return result

def update_ocorrencia(occ_id: int, payload: dict):
    """
    Atualiza a ocorrência e retorna o número de linhas afetadas.
    """
    sql = """
    UPDATE ocorrencia
       SET tipo_ocorrencia       = :tipo,
           data_inicio           = TO_TIMESTAMP(:data_inicio, 'YYYY-MM-DD"T"HH24:MI:SS'),
           data_fim              = CASE WHEN :data_fim IS NULL THEN NULL
                                      ELSE TO_TIMESTAMP(:data_fim, 'YYYY-MM-DD"T"HH24:MI:SS') END,
           severidade_ocorrencia = :severidade,
           fk_estacao_id_estacao = :id_estacao,
           fk_cco_id_cco         = :id_cco,
           status_ocorrencia     = :status
     WHERE id_ocorrencia         = :id
    """
    conn = get_conn()
    cur = conn.cursor()
    binds = {
      "tipo":        payload["tipo_ocorrencia"],
      "data_inicio": payload["data_inicio"],
      "data_fim":    payload.get("data_fim"),
      "severidade":  int(payload["severidade_ocorrencia"]),
      "id_estacao":  int(payload["id_estacao"]),
      "id_cco":      int(payload["id_cco"]),
      "status":      payload.get("status_ocorrencia", "ABERTO"),
      "id":          occ_id,
    }
    cur.execute(sql, binds)
    conn.commit()
    return cur.rowcount

def delete_ocorrencia(occ_id: int):
    """
    Deleta a ocorrência e retorna o número de linhas deletadas.
    """
    sql = "DELETE FROM ocorrencia WHERE id_ocorrencia = :id"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, {"id": occ_id})
    conn.commit()
    return cur.rowcount
