# main_app/middleware.py
from django.shortcuts import redirect
from django.contrib import messages
from .pyrebase_settings import auth
from .firebase_app import db

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = ['/login/', '/register/', '/admin/']

        if not request.path_info in allowed_paths:
            if not request.session.get('uid'):
                return redirect('login')
            else:
                # Fetch user role from Firestore
                uid = request.session.get('user_id')
                user_doc = db.collection('Users').document(uid).get()
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    request.role = user_data.get('role')
                else:
                    messages.error(request, "User profile not found.")
                    return redirect('login')
        response = self.get_response(request)
        return response
