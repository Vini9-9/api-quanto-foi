from datetime import date, datetime
from typing import List
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
            # Obter todos os produtos da referência base
            all_products = await self.repository.get_all()
            print('all_products', all_products)
            
            products = []
            # Iterar sobre os itens do dicionário (id é a chave do Firebase)
            for product_id, product_data in all_products.items():
                # Adiciona o ID do Firebase aos dados do produto
                product_data["id"] = str(product_id)  # Aqui usamos o ID real do Firebase!
                
                # --- Aplicar filtros ---
                # Filtro por local
                if filters.local and product_data.get("local") != filters.local:
                    continue
                    
                # Filtro por SKU
                if filters.sku and product_data.get("sku") != filters.sku:
                    continue
                    
                # Filtro por data de início
                if filters.data_inicio:
                    data_compra = datetime.fromisoformat(product_data["data"])
                    if data_compra < filters.data_inicio:
                        continue
                
                # Filtro por data de fim
                if filters.data_fim:
                    data_compra = datetime.fromisoformat(product_data["data"])
                    if data_compra > filters.data_fim:
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

# Instância global do serviço
product_service = ProductService()