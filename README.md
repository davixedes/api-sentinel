
# Documentação da API

Esta documentação detalha como utilizar a API REST, permitindo criar, listar, atualizar e excluir registros de **Funcionários**, **Atendimentos** e **Ocorrências**.

## URL Base

```
https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com
https://n88o6h6il8.execute-api.sa-east-1.amazonaws.com/dev
```

---

## Endpoints

## Funcionários

### 1. Criar um Funcionário (`POST`)

**URL:**

```
POST /funcionarios
```

**Exemplo de requisição com cURL:**

```bash
curl -X POST https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/funcionarios   -H "Content-Type: application/json"   -d '{
        "nome": "João Silva",
        "cargo": "Supervisor"
      }'
```

**Resposta esperada (201 Created):**

```json
{
  "id": "123",
  "mensagem": "Funcionário criado com sucesso!"
}
```

### 2. Listar Todos os Funcionários (`GET`)

```bash
curl -X GET https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/funcionarios
```

### 3. Buscar Funcionário por ID (`GET`)

```bash
curl -X GET https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/funcionarios/{id}
```

### 4. Atualizar Funcionário (`PUT`)

```bash
curl -X PUT https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/funcionarios/{id}   -H "Content-Type: application/json"   -d '{
        "nome": "João Silva",
        "cargo": "Gerente"
      }'
```

### 5. Deletar Funcionário (`DELETE`)

```bash
curl -X DELETE https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/funcionarios/{id}
```

## Atendimentos

### 1. Criar um Atendimento (`POST`)

```bash
curl -X POST https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/atendimentos   -H "Content-Type: application/json"   -d '{
        "funcId": "1",
        "ocorrId": "10",
        "descricao": "Atendimento realizado"
      }'
```

### 2. Listar Todos os Atendimentos (`GET`)

```bash
curl -X GET https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/atendimentos
```

### 3. Buscar Atendimento Específico (`GET`)

```bash
curl -X GET https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/atendimentos/{funcId}/{ocorrId}
```

### 4. Atualizar Atendimento (`PUT`)

```bash
curl -X PUT https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/atendimentos/{funcId}/{ocorrId}   -H "Content-Type: application/json"   -d '{
        "descricao": "Atendimento atualizado"
      }'
```

### 5. Deletar Atendimento (`DELETE`)

```bash
curl -X DELETE https://gkr7t959w0.execute-api.sa-east-1.amazonaws.com/atendimentos/{funcId}/{ocorrId}
```

## Ocorrências

### 1. Criar uma Ocorrência (`POST`)

```bash
curl -X POST https://n88o6h6il8.execute-api.sa-east-1.amazonaws.com/dev/ocorrencias   -H "Content-Type: application/json"   -d '{
        "tipo_ocorrencia": "Acidente",
        "data_inicio": "2025-04-07T12:00:00",
        "severidade": 1,
        "id_estacao": "1",
        "id_cco": "1",
        "status_ocorrencia": "Aberto"
      }'
```

### 2. Listar Todas as Ocorrências (`GET`)

```bash
curl -X GET https://n88o6h6il8.execute-api.sa-east-1.amazonaws.com/dev/ocorrencias
```

### 3. Buscar Ocorrência por ID (`GET`)

```bash
curl -X GET https://n88o6h6il8.execute-api.sa-east-1.amazonaws.com/dev/ocorrencias/{id}
```

### 4. Atualizar uma Ocorrência (`PUT`)

```bash
curl -X PUT https://n88o6h6il8.execute-api.sa-east-1.amazonaws.com/dev/ocorrencias/{id}   -H "Content-Type: application/json"   -d '{
        "tipo_ocorrencia": "Incidente",
        "data_inicio": "2025-04-07T14:00:00",
        "data_fim": "2025-04-07T15:00:00",
        "severidade_ocorrencia": 2,
        "id_estacao": "1",
        "id_cco": "1",
        "status_ocorrencia": "Fechado"
      }'
```

### 5. Deletar uma Ocorrência (`DELETE`)

```bash
curl -X DELETE https://n88o6h6il8.execute-api.sa-east-1.amazonaws.com/dev/ocorrencias/{id}
```

## Tratamento de Erros

Em caso de erro, a API retorna:

```json
{
  "error": "Mensagem explicativa do erro"
}
```

**Status HTTP comuns:**

- `400 Bad Request`: Dados inválidos.
- `404 Not Found`: Recurso não encontrado.
- `500 Internal Server Error`: Erro interno.
