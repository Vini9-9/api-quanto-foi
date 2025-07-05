from datetime import date, datetime
from typing import Dict, List, Optional
from models import Product, ProductCreate, ProductFilter
import logging
from repository import FirebaseRepository

logger = logging.getLogger(__name__)

class ProductService:
    _instance = None
    """Serviço para gerenciar produtos no Firebase"""
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProductService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        print("################# Iniciando Service #################")
        self.repository = FirebaseRepository()
    
    def get_info(self):
            return self.repository.get_info()

    async def create_product(self, product_data: ProductCreate) -> Product:
        """Valida dados e cria produto."""
        try:
            # Converte o modelo Pydantic para dicionário (modificável)
            product_dict = product_data.model_dump()
            
            # Atribui data atual se não existir
            if not product_dict.get("data"):
                product_dict["data"] = date.today().isoformat()
            
            # Cria via repository (envia o dicionário, não o modelo)
            created_data = await self.repository.create_product(product_dict)
            return Product(**created_data)
        
        except Exception as e:
            logger.error(f"Erro ao criar produto: {str(e)}")
            raise
    
    async def get_products(self, filters: ProductFilter) -> List[Product]:
        """Busca produtos com filtros"""
        try:
            if filters.sku:
                products_data = await self.repository.get_by_sku(filters.sku)
                return [Product(**p) for p in products_data]
            
            if filters.data_inicio:
                products_data = await self.repository.get_by_date(filters.data_inicio)
                return [Product(**p) for p in products_data.values()]
            
            # Obter todos os produtos da referência base
            all_products = await self.repository.get_all()
            
            products = []
            # Iterar sobre os itens do dicionário (id é a chave do Firebase)
            for product_id, product_data in all_products.items():
                # Adiciona o ID do Firebase aos dados do produto
                product_data["id"] = str(product_id)  # Aqui usamos o ID real do Firebase!
                
                # --- Aplicar filtros ---
                # Filtro por local
                if filters.local and product_data.get("local") != filters.local:
                    continue

                # Filtro por descrição (case-insensitive)
                if filters.descricao:
                    descricao_produto = product_data.get("descricao", "").lower()
                    if filters.descricao.lower() not in descricao_produto:
                        continue
                
                # Adiciona o produto filtrado à lista
                products.append(Product(**product_data))
                
                # Limita resultados se necessário
                if filters.limite and len(products) >= filters.limite:
                    break
            
            return products
        
        except Exception as e:
            logger.error(f"Erro ao buscar produtos: {str(e)}")
            raise

    def _matches_filters(self, product_data: Dict, filters: ProductFilter) -> bool:
        """Aplica todos os filtros não otimizados em memória."""
        # Filtro por local
        if filters.local and product_data.get("local") != filters.local:
            return False
            
        # Filtro por preço mínimo
        if filters.preco_min is not None:
            preco = product_data.get("preco")
            if preco is None or preco < filters.preco_min:
                return False
        
        # Filtro por preço máximo
        if filters.preco_max is not None:
            preco = product_data.get("preco")
            if preco is None or preco > filters.preco_max:
                return False
        
        # Filtro por data de início
        if filters.data_inicio:
            data_produto = product_data.get("data")
            if not data_produto or datetime.fromisoformat(data_produto) < datetime.fromisoformat(filters.data_inicio):
                return False
        
        # Filtro por data de fim
        if filters.data_fim:
            data_produto = product_data.get("data")
            if not data_produto or datetime.fromisoformat(data_produto) > datetime.fromisoformat(filters.data_fim):
                return False
        
        # Filtro por descrição (case insensitive)
        if filters.descricao:
            descricao_produto = product_data.get("descricao", "").lower()
            if filters.descricao.lower() not in descricao_produto:
                return False
        
        return True

# Instância global do serviço
product_service = ProductService()