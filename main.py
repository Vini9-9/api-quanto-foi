from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
from datetime import date
import logging

from models import Product, ProductCreate, ProductFilter, ProductResponse
from services import product_service

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="API de Compras de Mercado",
    description="API para gerenciar compras de mercado com integração ao Firebase",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "API de Compras de Mercado",
        "version": "1.0.0",
        "endpoints": {
            "criar_produto": "POST /produtos",
            "listar_produtos": "GET /produtos",
            "buscar_produto": "GET /produtos/{id}",
            "documentacao": "GET /docs"
        }
    }

@app.post("/produtos", response_model=Product)
async def criar_produto(produto: ProductCreate):
    """Cria um novo produto"""
    try:
        new_product = await product_service.create_product(produto)
        logger.info(f"Produto criado com sucesso: {new_product.id}")
        return new_product
    except Exception as e:
        logger.error(f"Erro ao criar produto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar produto: {str(e)}")

@app.get("/produtos", response_model=ProductResponse)
async def listar_produtos(
    local: Optional[str] = Query(None, description="Filtrar por local da compra"),
    descricao: Optional[str] = Query(None, description="Filtrar por descrição do produto"),
    sku: Optional[str] = Query(None, description="Filtrar por SKU do produto"),
    data_inicio: Optional[date] = Query(None, description="Data de início (ISO format)"),
    data_fim: Optional[date] = Query(None, description="Data de fim (ISO format)"),
    limite: Optional[int] = Query(100, ge=1, le=1000, description="Limite de resultados")
):
    """Lista produtos com filtros opcionais"""
    try:
        # Criar filtros
        filters = ProductFilter(
            local=local,
            descricao=descricao,
            sku=sku,
            data_inicio=data_inicio,
            data_fim=data_fim,
            limite=limite
        )
        
        # Buscar produtos
        products = await product_service.get_products(filters)
        total = len(products)
        
        # Preparar resposta
        response = ProductResponse(
            produtos=products,
            total=total,
            filtros_aplicados={
                "local": local,
                "descricao": descricao,
                "sku": sku,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "limite": limite
            }
        )
        
        logger.info(f"Produtos encontrados: {total}")
        return response
        
    except Exception as e:
        logger.error(f"Erro ao listar produtos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")

@app.get("/produtos/{product_id}", response_model=Product)
async def buscar_produto(product_id: str):
    """Busca um produto específico por ID"""
    try:
        product = await product_service.get_product_by_id(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        logger.info(f"Produto encontrado: {product_id}")
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar produto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produto: {str(e)}")

@app.get("/health")
async def health_check():
    """Verifica a saúde da API"""
    try:
        # Teste simples de conexão com Firebase
        test_query = product_service.get_info()
        if(test_query):
        
            return {
                "status": "healthy",
                "timestamp": datetime.now(),
                "database": "connected"
            }
    except Exception as e:
        logger.error(f"Erro no health check: {str(e)}")
        raise HTTPException(status_code=503, detail="Serviço indisponível")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)