import firebase_admin
from firebase_admin import db, credentials
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

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
        """Obtém todos os produtos (para filtros complexos)."""
        return self._base_ref.get() or {}
    
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