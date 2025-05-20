import os
import oracledb

def get_conn():
    """Retorna uma conexão Oracle usando as variáveis de ambiente."""
    return oracledb.connect(
        user=os.environ['ORACLE_USER'],
        password=os.environ['ORACLE_PASSWORD'],
        dsn=os.environ['ORACLE_DSN']
    )

def create_atendimento(payload: dict):
    """
    Cria um vínculo funcionário↔ocorrência.
    Espera keys:
      - func_id   (int)
      - ocorr_id  (int)
      - data_inicio_atendimento (str ISO 'YYYY-MM-DD')
    """
    sql = """
    INSERT INTO func_ocorr_atende (
      fk_funcionario_id_funcionario,
      fk_ocorrencia_id_ocorrencia,
      data_inicio_atendimento
    ) VALUES (
      :1, :2, TO_DATE(:3,'YYYY-MM-DD')
    )
    """
    conn = get_conn()
    cur = conn.cursor()
    params = (
        int(payload['func_id']),
        int(payload['ocorr_id']),
        payload['data_inicio_atendimento']
    )
    cur.execute(sql, params)
    conn.commit()

def list_atendimentos():
    """
    Retorna todos os atendimentos como lista de dicts.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
      SELECT
        fk_funcionario_id_funcionario AS func_id,
        fk_ocorrencia_id_ocorrencia   AS ocorr_id,
        data_inicio_atendimento
      FROM func_ocorr_atende
    """)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]

def get_atendimento(func_id: int, ocorr_id: int):
    """
    Recupera um atendimento específico pela dupla (func_id, ocorr_id).
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
      SELECT
        fk_funcionario_id_funcionario AS func_id,
        fk_ocorrencia_id_ocorrencia   AS ocorr_id,
        data_inicio_atendimento
      FROM func_ocorr_atende
      WHERE fk_funcionario_id_funcionario = :1
        AND fk_ocorrencia_id_ocorrencia   = :2
    """, (func_id, ocorr_id))
    row = cur.fetchone()
    if not row:
        return None
    cols = [c[0] for c in cur.description]
    return dict(zip(cols, row))

def update_atendimento(func_id: int, ocorr_id: int, payload: dict):
    """
    Atualiza data_inicio_atendimento de um vínculo.
    Retorna número de linhas afetadas.
    """
    sql = """
    UPDATE func_ocorr_atende
       SET data_inicio_atendimento = TO_DATE(:3,'YYYY-MM-DD')
     WHERE fk_funcionario_id_funcionario = :1
       AND fk_ocorrencia_id_ocorrencia   = :2
    """
    conn = get_conn()
    cur = conn.cursor()
    params = (
        func_id,
        ocorr_id,
        payload['data_inicio_atendimento']
    )
    cur.execute(sql, params)
    conn.commit()
    return cur.rowcount

def delete_atendimento(func_id: int, ocorr_id: int):
    """
    Remove o vínculo funcionário↔ocorrência.
    Retorna número de linhas deletadas.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
      DELETE FROM func_ocorr_atende
       WHERE fk_funcionario_id_funcionario = :1
         AND fk_ocorrencia_id_ocorrencia   = :2
    """, (func_id, ocorr_id))
    conn.commit()
    return cur.rowcount
