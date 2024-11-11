import firebase_admin
from firebase_admin import credentials, firestore

# Path to your service account key JSON file
cred = credentials.Certificate('E:/SynologyDrive/MIT Studies/Database Subject Output/Development folder/document-tracking-system/dts_project/serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_app = firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()
