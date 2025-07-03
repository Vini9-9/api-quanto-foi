import firebase_admin
from firebase_admin import db, credentials
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

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

    def get_info(self):
        return db.reference('info').get()
    
    def get_products(self):
        return db.reference('produtos').get() or {}