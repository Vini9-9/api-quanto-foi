from datetime import datetime
from typing import List, Optional
# from firebase_admin import firestore
from models import Product, ProductCreate, ProductFilter
# from firebase_config import db
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

    # async def create_product(self, product_data: ProductCreate) -> Product:
    #     """Cria um novo produto no Firebase"""
    #     try:
    #         # Preparar dados do produto
    #         product_dict = {
    #             "data_hora_compra": datetime.now(),
    #             "local_compra": product_data.local_compra,
    #             "descricao": product_data.descricao,
    #             "sku": product_data.sku,
    #             "preco": product_data.preco
    #         }
            
    #         # Salvar no Firebase
    #         doc_ref = self.collection.add(product_dict)
    #         product_id = doc_ref[1].id
            
    #         # Retornar produto criado
    #         return Product(
    #             id=product_id,
    #             **product_dict
    #         )
            
    #     except Exception as e:
    #         logger.error(f"Erro ao criar produto: {str(e)}")
    #         raise
    
    # async def get_products(self, filters: ProductFilter) -> List[Product]:
    #     """Busca produtos com filtros"""
    #     try:
    #         query = self.collection
            
    #         # Aplicar filtros
    #         if filters.local_compra:
    #             query = query.where("local_compra", "==", filters.local_compra)
            
    #         if filters.sku:
    #             query = query.where("sku", "==", filters.sku)
            
    #         if filters.preco_min is not None:
    #             query = query.where("preco", ">=", filters.preco_min)
            
    #         if filters.preco_max is not None:
    #             query = query.where("preco", "<=", filters.preco_max)
            
    #         if filters.data_inicio:
    #             query = query.where("data_hora_compra", ">=", filters.data_inicio)
            
    #         if filters.data_fim:
    #             query = query.where("data_hora_compra", "<=", filters.data_fim)
            
    #         # Limitar resultados
    #         query = query.limit(filters.limite)
            
    #         # Executar query
    #         docs = query.stream()
            
    #         # Converter para lista de produtos
    #         products = []
    #         for doc in docs:
    #             product_data = doc.to_dict()
    #             product_data["id"] = doc.id
                
    #             # Filtro por descrição (não suportado nativamente pelo Firestore)
    #             if filters.descricao:
    #                 if filters.descricao.lower() not in product_data["descricao"].lower():
    #                     continue
                
    #             products.append(Product(**product_data))
            
    #         return products
            
    #     except Exception as e:
    #         logger.error(f"Erro ao buscar produtos: {str(e)}")
    #         raise
    
    # async def get_product_by_id(self, product_id: str) -> Optional[Product]:
    #     """Busca um produto por ID"""
    #     try:
    #         doc = self.collection.document(product_id).get()
            
    #         if doc.exists:
    #             product_data = doc.to_dict()
    #             product_data["id"] = doc.id
    #             return Product(**product_data)
            
    #         return None
            
    #     except Exception as e:
    #         logger.error(f"Erro ao buscar produto por ID: {str(e)}")
    #         raise
    
    # async def count_products(self, filters: ProductFilter) -> int:
    #     """Conta o número de produtos com os filtros aplicados"""
    #     try:
    #         products = await self.get_products(filters)
    #         return len(products)
            
    #     except Exception as e:
    #         logger.error(f"Erro ao contar produtos: {str(e)}")
    #         raise

# Instância global do serviço
product_service = ProductService()