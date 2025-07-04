import firebase_admin
from firebase_admin import db, credentials
from dotenv import load_dotenv
import os
from typing import Dict, List

load_dotenv()

firebase_cred_path = os.getenv('FIREBASE_CRED_PATH')
database_url = os.getenv('DATABASE_URL')

class FirebaseRepository:
    def __init__(self):
        print("################# Iniciando Repository #################")
        cred = credentials.Certificate(firebase_cred_path)
        firebase_admin.initialize_app(cred, {
            "databaseURL": database_url
        })
        self._base_ref = db.reference("produtos")
        self._index_ref = db.reference("indices")

    def get_info(self):
        return db.reference('info').get()
    
    async def get_all(self) -> Dict[str, Dict]:
        """Obtém todos os produtos"""
        return self._base_ref.get() or {}
    
    async def get_by_sku(self, sku: str) -> List[Dict]:
        """Retorna lista de produtos com o SKU especificado."""
        product_ids = self._index_ref.child(f"por_sku/{sku}").get() or {}
        return [
            {"id": pid, **self._base_ref.child(pid).get()}
            for pid in product_ids.keys()
        ]
    
    async def get_by_date(self, date: str) -> Dict[str, Dict]:
        """Obtém produtos por data"""
        product_ids = self._index_ref.child(f"por_data/{date}").get() or {}
        return {
            pid: self._base_ref.child(pid).get()
            for pid in product_ids.keys()
        }
    
    async def create_product(self, product_data: Dict) -> Dict:
        """Cria produto e atualiza índices."""
        new_ref = self._base_ref.push()
        product_id = new_ref.key
        product_data["id"] = product_id
        
        # Atualização atômica
        updates = {
            f"produtos/{product_id}": product_data,
            f"indices/por_sku/{product_data['sku']}/{product_id}": True,
            f"indices/por_data/{product_data['data']}/{product_id}": True
        }
        
        db.reference().update(updates)
        return product_data