# Documentação da API de Ocorrências

Essa documentação detalha como utilizar a API REST de ocorrências, permitindo criar, listar, atualizar e excluir ocorrências, incluindo o novo campo de status.

## URL Base

```
https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com
```

---

## Endpoints

### 1. Criar uma Ocorrência (`POST`)

**URL:**
```
POST /ocorrencia
```

**Payload (JSON):**

```json
{
  "tipo_ocorrencia": "Acidente",
  "data_inicio": "2025-04-07T12:00:00",
  "severidade": 1,
  "id_estacao": "1",
  "id_cco": "1",
  "status_ocorrencia": "Aberto"
}
```

**Exemplo de requisição com cURL:**

```bash
curl -X POST https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/ocorrencia \
  -H "Content-Type: application/json" \
  -d '{
        "tipo_ocorrencia": "Acidente",
        "data_inicio": "2025-04-07T12:00:00",
        "severidade": 1,
        "id_estacao": "1",
        "id_cco": "1",
        "status_ocorrencia": "Aberto"
      }'
```

**Resposta esperada (201 Created):**

```json
{
  "id": "f226abb1-9cb5-4af8-87ba-435740213764",
  "mensagem": "Ocorrência criada com sucesso!"
}
```

---

### 2. Listar Todas as Ocorrências (`GET`)

**URL:**
```
GET /ocorrencia
```

**Exemplo de requisição com cURL:**

```bash
curl -X GET https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/ocorrencia
```

**Resposta esperada (200 OK):**

```json
[
  {
    "ID_OCORRENCIA": "f226abb1-9cb5-4af8-87ba-435740213764",
    "TIPO_OCORRENCIA": "Acidente",
    "DATA_INICIO": "2025-04-07 12:00:00",
    "DATA_FIM": null,
    "SEVERIDADE_OCORRENCIA": 1,
    "FK_ESTACAO_ID_ESTACAO": 1,
    "FK_CCO_ID_CCO": 1,
    "STATUS_OCORRENCIA": "Aberto"
  }
]
```

---

### 3. Atualizar uma Ocorrência (`PUT`)

**URL:**
```
PUT /ocorrencia/{id_ocorrencia}
```

Substitua `{id_ocorrencia}` pelo ID real da ocorrência.

**Payload (JSON):**

```json
{
  "tipo_ocorrencia": "Incidente",
  "data_inicio": "2025-04-07T14:00:00",
  "data_fim": "2025-04-07T15:00:00",
  "severidade_ocorrencia": 2,
  "id_estacao": "1",
  "id_cco": "1",
  "status_ocorrencia": "Fechado"
}
```

**Exemplo de requisição com cURL:**

```bash
curl -X PUT https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/ocorrencia/f226abb1-9cb5-4af8-87ba-435740213764 \
  -H "Content-Type: application/json" \
  -d '{
        "tipo_ocorrencia": "Incidente",
        "data_inicio": "2025-04-07T14:00:00",
        "data_fim": "2025-04-07T15:00:00",
        "severidade_ocorrencia": 2,
        "id_estacao": "1",
        "id_cco": "1",
        "status_ocorrencia": "Fechado"
      }'
```

**Resposta esperada (204 No Content):** Sem conteúdo no corpo da resposta.

---

### 4. Deletar uma Ocorrência (`DELETE`)

**URL:**
```
DELETE /ocorrencia/{id_ocorrencia}
```

Substitua `{id_ocorrencia}` pelo ID real da ocorrência.

**Exemplo de requisição com cURL:**

```bash
curl -X DELETE https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/ocorrencia/f226abb1-9cb5-4af8-87ba-435740213764
```

**Resposta esperada (204 No Content):** Sem conteúdo no corpo da resposta.

---

## Tratamento de Erros

Em casos de erro, a API retorna mensagens no seguinte formato:

```json
{
  "error": "Mensagem explicativa do erro"
}
```

Exemplos comuns de status HTTP retornados em erros:

- **400 Bad Request:** Requisição inválida (falta de parâmetros obrigatórios).
- **404 Not Found:** Registro não encontrado.
- **500 Internal Server Error:** Erro interno do servidor.

