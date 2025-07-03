# API de Compras de Mercado

API REST em Python para gerenciar compras de mercado com integração ao Firebase Firestore.

## Funcionalidades

- ✅ Criar produtos de compra
- ✅ Listar produtos com filtros avançados
- ✅ Buscar produto por ID
- ✅ Integração completa com Firebase Firestore
- ✅ Validação de dados com Pydantic
- ✅ Documentação automática com Swagger

## Estrutura do Produto

```json
{
  "id": "string (gerado automaticamente)",
  "data_hora_compra": "datetime (gerado automaticamente)",
  "local_compra": "string",
  "descricao": "string",
  "sku": "string",
  "preco": "float"
}
```

## Configuração

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar a aplicação

```bash
python main.py
```

A API estará disponível em `http://localhost:8000`

## Endpoints

### POST /produtos
Cria um novo produto

**Body:**
```json
{
  "local_compra": "Supermercado XYZ",
  "descricao": "Leite integral 1L",
  "sku": "LEITE-001",
  "preco": 4.50
}
```

### GET /produtos
Lista produtos com filtros opcionais

**Query Parameters:**
- `local_compra`: Filtrar por local da compra
- `descricao`: Filtrar por descrição do produto
- `sku`: Filtrar por SKU do produto
- `preco_min`: Preço mínimo
- `preco_max`: Preço máximo
- `data_inicio`: Data de início (ISO format)
- `data_fim`: Data de fim (ISO format)
- `limite`: Limite de resultados (padrão: 100)

### GET /produtos/{id}
Busca um produto específico por ID

### GET /health
Verifica a saúde da API

## Documentação

A documentação interativa está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Exemplos de Uso

### Criar um produto
```bash
curl -X POST "http://localhost:8000/produtos" \
  -H "Content-Type: application/json" \
  -d '{
    "local_compra": "Supermercado ABC",
    "descricao": "Arroz branco 5kg",
    "sku": "ARR-001",
    "preco": 12.90
  }'
```

### Listar produtos
```bash
curl "http://localhost:8000/produtos"
```

### Filtrar produtos por local
```bash
curl "http://localhost:8000/produtos?local_compra=Supermercado%20ABC"
```

### Filtrar produtos por faixa de preço
```bash
curl "http://localhost:8000/produtos?preco_min=10.00&preco_max=20.00"
```

## Estrutura do Projeto

```
.
├── main.py              # Aplicação FastAPI principal
├── models.py            # Modelos Pydantic
├── services.py          # Lógica de negócio
├── firebase_config.py   # Configuração do Firebase
├── requirements.txt     # Dependências
├── .env.example        # Exemplo de variáveis de ambiente
└── README.md           # Documentação
```

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **Firebase Firestore**: Banco de dados NoSQL
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI
- **Python-dotenv**: Gerenciamento de variáveis de ambiente