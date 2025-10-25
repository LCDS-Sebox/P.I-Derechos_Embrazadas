from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

def home(request):
    """Vista principal"""
    return render(request, 'index.html')

def login_view(request):
    """Vista para login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'¡Bienvenida {user.username}!')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
        
        return redirect('home')
    
    return redirect('home')

def logout_view(request):
    """Vista para logout"""
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, 'Sesión cerrada exitosamente')
    
    return redirect('home')