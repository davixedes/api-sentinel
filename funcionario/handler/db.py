from typing import Optional
import os
import oracledb

def get_conn():
    """
    Retorna uma conexão Oracle usando as variáveis de ambiente.
    """
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

def create_funcionario(payload: dict) -> int:
    """
    Insere um funcionário e retorna o id gerado.
    Espera as chaves em payload:
      - nome              (str)
      - status            (int)
      - sexo_funcionario  (str ou None)
      - id_cargo          (int ou None)
    """
    sql = """
    INSERT INTO funcionario (
        nome,
        status,
        sexo_funcionario,
        fk_cargo_id_cargo
    ) VALUES (
        :1, :2, :3, :4
    )
    RETURNING id_funcionario INTO :5
    """
    conn = get_conn()
    cur = conn.cursor()
    # bind de saída
    id_var = cur.var(oracledb.DB_TYPE_NUMBER)

    params = (
        payload['nome'],
        int(payload['status']),
        payload.get('sexo_funcionario'),
        payload.get('id_cargo'),
        id_var
    )

    cur.execute(sql, params)
    conn.commit()
    return int(id_var.getvalue()[0])

def update_funcionario(func_id: int, payload: dict) -> int:
    """
    Atualiza um funcionário pelo id e retorna o número de linhas afetadas.
    Payload com as mesmas chaves do create_funcionario.
    """
    sql = """
    UPDATE funcionario
       SET nome              = :1,
           status            = :2,
           sexo_funcionario  = :3,
           fk_cargo_id_cargo = :4
     WHERE id_funcionario    = :5
    """
    conn = get_conn()
    cur = conn.cursor()
    params = (
        payload['nome'],
        int(payload['status']),
        payload.get('sexo_funcionario'),
        payload.get('id_cargo'),
        func_id
    )
    cur.execute(sql, params)
    conn.commit()
    return cur.rowcount

def delete_funcionario(func_id: int) -> int:
    """
    Remove o funcionário de id fornecido.
    Retorna o número de linhas deletadas.
    """
    sql = "DELETE FROM funcionario WHERE id_funcionario = :1"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, (func_id,))
    conn.commit()
    return cur.rowcount

def list_funcionarios() -> list[dict]:
    """
    Retorna todos os funcionários como lista de dicionários.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM funcionario")
    rows = cur.fetchall()
    cols = [col[0] for col in cur.description]
    return [dict(zip(cols, row)) for row in rows]

def get_funcionario_by_id(func_id: int) -> Optional[dict]:
    """
    Recupera um único funcionário pelo ID.
    Retorna um dicionário com as colunas ou None se não existir.
    """
    conn = get_conn()
    cur = conn.cursor()
    sql = """
    SELECT
      id_funcionario,
      nome,
      status,
      sexo_funcionario,
      fk_cargo_id_cargo
    FROM funcionario
     WHERE id_funcionario = :1
    """
    cur.execute(sql, (func_id,))
    row = cur.fetchone()
    if row is None:
        return None

    cols = [d[0] for d in cur.description]
    return dict(zip(cols, row))
