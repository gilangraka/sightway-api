import firebase_admin
from firebase_admin import credentials, db
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
cred_path = os.path.join(base_dir, 'firebase_credential.json')

cred = credentials.Certificate(cred_path)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sightway-9f360-default-rtdb.firebaseio.com/'
})