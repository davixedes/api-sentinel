import os
import oracledb

def get_conn():
    try:
        conn = oracledb.connect(
            user=os.environ['ORACLE_USER'],
            password=os.environ['ORACLE_PASSWORD'],
            dsn=os.environ['ORACLE_DSN']
        )
        return conn
    except oracledb.Error as e:
        print("Erro ao conectar:", e)
        raise

def create_ocorrencia(payload: dict) -> int:
    """
    Insere uma ocorrência e retorna o id gerado pelo IDENTITY.
    Espera as chaves:
      - tipo_ocorrencia (str)
      - data_inicio      (str ISO 'YYYY-MM-DD"T"HH24:MI:SS')
      - data_fim         (str ISO ou None)
      - severidade_ocorrencia (int)
      - id_estacao       (int)
      - id_cco           (int)
      - status_ocorrencia(str)
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
        :1,
        TO_TIMESTAMP(:2, 'YYYY-MM-DD"T"HH24:MI:SS'),
        CASE WHEN :3 IS NULL THEN NULL 
             ELSE TO_TIMESTAMP(:3, 'YYYY-MM-DD"T"HH24:MI:SS') END,
        :4,
        :5,
        :6,
        :7
    )
    RETURNING id_ocorrencia INTO :8
    """

    conn = get_conn()
    cur = conn.cursor()

    # variavel de saída para o RETURNING
    id_var = cur.var(oracledb.DB_TYPE_NUMBER)

    params = (
        payload['tipo_ocorrencia'],
        payload['data_inicio'],
        payload.get('data_fim'),
        int(payload['severidade_ocorrencia']),
        int(payload['id_estacao']),
        int(payload['id_cco']),
        payload.get('status_ocorrencia', 'ABERTO'),
        id_var
    )

    cur.execute(sql, params)
    conn.commit()

    # retorna o valor como int
    return int(id_var.getvalue()[0])

def update_ocorrencia(occ_id: int, payload: dict) -> int:
    """
    Atualiza uma ocorrência e retorna número de linhas alteradas.
    """
    sql = """
    UPDATE ocorrencia
       SET tipo_ocorrencia       = :1,
           data_inicio           = TO_TIMESTAMP(:2, 'YYYY-MM-DD"T"HH24:MI:SS'),
           data_fim              = CASE WHEN :3 IS NULL THEN NULL 
                                         ELSE TO_TIMESTAMP(:3, 'YYYY-MM-DD"T"HH24:MI:SS') END,
           severidade_ocorrencia = :4,
           fk_estacao_id_estacao = :5,
           fk_cco_id_cco         = :6,
           status_ocorrencia     = :7
     WHERE id_ocorrencia = :8
    """

    conn = get_conn()
    cur = conn.cursor()

    params = (
        payload['tipo_ocorrencia'],
        payload['data_inicio'],
        payload.get('data_fim'),
        int(payload['severidade_ocorrencia']),
        int(payload['id_estacao']),
        int(payload['id_cco']),
        payload.get('status_ocorrencia', 'ABERTO'),
        occ_id
    )

    cur.execute(sql, params)
    conn.commit()
    return cur.rowcount


def delete_ocorrencia(occ_id: int) -> int:
    """
    Remove a ocorrência de id fornecido.
    Retorna o número de linhas deletadas.
    """
    sql = "DELETE FROM ocorrencia WHERE id_ocorrencia = :1"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, (occ_id,))
    conn.commit()
    return cur.rowcount


def list_ocorrencias() -> list[dict]:
    """
    Retorna todas as ocorrências como lista de dicionários.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ocorrencia")
    rows = cur.fetchall()
    cols = [col[0] for col in cur.description]
    # Monta lista de dicts
    ocorrencias = [dict(zip(cols, row)) for row in rows]
    return ocorrencias