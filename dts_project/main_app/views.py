from .firebase_app import db
from django.shortcuts import render, redirect
from django.contrib import messages
from .pyrebase_settings import auth

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')  # Get role from form

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']

            # Create user profile in Firestore
            data = {
                'email': email,
                'role': role
            }
            db.collection('Users').document(uid).set(data)

            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        except Exception as e:
            error_message = str(e)
            messages.error(request, f"Error: {error_message}")
            return redirect('register')
    return render(request, 'register.html')

def admin_dashboard(request):
    if not request.session.get('uid'):
        return redirect('login')
    if request.role != 'Administrator':
        messages.error(request, "You do not have permission to access this page.")
        return redirect('dashboard')
    return render(request, 'admin_dashboard.html')



def dashboard(request):
    if not request.session.get('uid'):
        return redirect('login')
    return render(request, 'dashboard.html')

def logout(request):
    try:
        del request.session['uid']
        del request.session['refreshToken']
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('login')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            uid = user['localId']

            # Store user token in session
            request.session['uid'] = user['idToken']
            request.session['refreshToken'] = user['refreshToken']
            request.session['user_id'] = uid  # Store UID for later use

            return redirect('dashboard')
        except Exception as e:
            error_message = str(e)
            messages.error(request, f"Invalid credentials: {error_message}")
            return redirect('login')
    return render(request, 'login.html')

def home(request):
    # Test Firestore Connection
    doc_ref = db.collection('test_collection').document('test_document')
    doc_ref.set({
        'name': 'Test Document',
        'message': 'Hello, Firestore!'
    })

    # Retrieve Document
    doc = doc_ref.get()
    data = doc.to_dict()

    return render(request, 'home.html', {'data': data})
