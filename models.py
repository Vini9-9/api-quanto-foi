from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

class ProductCreate(BaseModel):
    """Modelo para criar um novo produto"""
    local_compra: str = Field(..., description="Local onde foi feita a compra")
    descricao: str = Field(..., description="Descrição do produto")
    sku: str = Field(..., description="SKU do produto")
    preco: float = Field(..., gt=0, description="Preço pago pelo produto")

class Product(BaseModel):
    """Modelo completo do produto"""
    id: str = Field(..., description="ID único do produto")
    data_hora_compra: datetime = Field(..., description="Data e hora da compra")
    local_compra: str = Field(..., description="Local onde foi feita a compra")
    descricao: str = Field(..., description="Descrição do produto")
    sku: str = Field(..., description="SKU do produto")
    preco: float = Field(..., gt=0, description="Preço pago pelo produto")

class ProductFilter(BaseModel):
    """Filtros para buscar produtos"""
    local_compra: Optional[str] = None
    descricao: Optional[str] = None
    sku: Optional[str] = None
    preco_min: Optional[float] = None
    preco_max: Optional[float] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    limite: Optional[int] = Field(default=100, le=1000)

class ProductResponse(BaseModel):
    """Resposta da API com produtos"""
    produtos: list[Product]
    total: int
    filtros_aplicados: dict