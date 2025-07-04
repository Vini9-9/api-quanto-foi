from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    """Modelo para criar um novo produto"""
    data: Optional[str] = Field(..., description="Data da compra")
    local: str = Field(..., description="Local onde foi feita a compra")
    descricao: str = Field(..., description="Descrição do produto")
    sku: str = Field(..., description="SKU do produto")
    preco: float = Field(..., gt=0, description="Preço pago pelo produto")

class Product(BaseModel):
    """Modelo completo do produto"""
    id: str = Field(..., description="ID único do produto")
    data: str = Field(..., description="Data da compra")
    local: str = Field(..., description="Local onde foi feita a compra")
    descricao: str = Field(..., description="Descrição do produto")
    sku: str = Field(..., description="SKU do produto")
    preco: float = Field(..., gt=0, description="Preço pago pelo produto")

class ProductFilter(BaseModel):
    """Filtros para buscar produtos"""
    local: Optional[str] = None
    descricao: Optional[str] = None
    sku: Optional[str] = None
    data_inicio: Optional[str] = None
    data_fim: Optional[str] = None
    limite: Optional[int] = Field(default=100, le=1000)

class ProductResponse(BaseModel):
    """Resposta da API com produtos"""
    produtos: list[Product]
    total: int
    filtros_aplicados: dict