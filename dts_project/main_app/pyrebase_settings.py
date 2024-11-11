# main_app/pyrebase_settings.py
import pyrebase
from .firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
