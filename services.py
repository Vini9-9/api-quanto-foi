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
    
    async def get_products(self, filters: ProductFilter) -> List[Product]:
        """Busca produtos com filtros"""
        try:
            # Obter todos os produtos da referência base
            all_products = self.repository.get_products()
            print('all_products', all_products)
            
            products = []
            if isinstance(all_products, list):
                for product_data in all_products:
                    product_data["id"] = str(product_data.get("id"))
                    # Aplicar filtros
                    if filters.local_compra and product_data.get("local_compra") != filters.local_compra:
                        continue
                        
                    if filters.sku and product_data.get("sku") != filters.sku:
                        continue
                        
                    if filters.preco_min is not None and product_data.get("preco", 0) < filters.preco_min:
                        continue
                        
                    if filters.preco_max is not None and product_data.get("preco", float('inf')) > filters.preco_max:
                        continue
                        
                    if filters.data_inicio:
                        # Converte a string ISO do Firebase para datetime
                        data_compra = datetime.fromisoformat(product_data["data_hora_compra"])
                        if data_compra < filters.data_inicio:
                            continue
                        
                    if filters.data_fim:
                        data_compra = datetime.fromisoformat(product_data["data_hora_compra"])
                        if data_compra > filters.data_fim:
                            continue
                        
                    # Filtro por descrição
                    if filters.descricao and filters.descricao.lower() not in product_data.get("descricao", "").lower():
                        continue
                        
                    products.append(Product(**product_data))
                    
                    # Limitar resultados
                    if filters.limite and len(products) >= filters.limite:
                        break
                    
            return products
        
        except Exception as e:
            logger.error(f"Erro ao buscar produtos: {str(e)}")
            raise
    
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