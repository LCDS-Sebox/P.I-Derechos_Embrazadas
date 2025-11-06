from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import CasoProblema, Thread, Post, Document, Tag
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .forms import ThreadForm, PostForm, RegisterForm

def home(request):
    """Vista principal"""
    # Obtener todos los casos activos agrupados por categoría
    casos = CasoProblema.objects.filter(activo=True)
    return render(request, 'index.html', {'casos': casos})

def caso_detalle(request, caso_id):
    """Vista para mostrar el detalle de un caso específico"""
    caso = get_object_or_404(CasoProblema, id=caso_id, activo=True)
    
    # Obtener casos relacionados (misma categoría)
    casos_relacionados = CasoProblema.objects.filter(
        categoria=caso.categoria, 
        activo=True
    ).exclude(id=caso_id)[:3]
    
    context = {
        'caso': caso,
        'casos_relacionados': casos_relacionados
    }
    return render(request, 'caso_detalle.html', context)

def casos_por_categoria(request, categoria):
    """Vista para mostrar todos los casos de una categoría"""
    casos = CasoProblema.objects.filter(categoria=categoria, activo=True)
    
    categoria_nombres = {
        'legal': 'Protección Legal',
        'medica': 'Atención Médica',
        'laboral': 'Derechos Laborales',
        'licencias': 'Licencias Maternales',
    }
    
    context = {
        'casos': casos,
        'categoria': categoria,
        'categoria_nombre': categoria_nombres.get(categoria, categoria)
    }
    return render(request, 'caso_categoria.html', context)

def register_view(request):
    """Vista para registro de usuarios"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f'¡Bienvenida {user.username}! Tu cuenta ha sido creada.')
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error[0])
    return redirect('home')

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


def foro_index(request):
    """Listado de hilos del foro"""
    threads = Thread.objects.all().select_related('author')
    return render(request, 'foro_index.html', {'threads': threads})


def foro_thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.select_related('author').all()
    reply_form = PostForm()
    return render(request, 'foro_thread.html', {'thread': thread, 'posts': posts, 'reply_form': reply_form})


@login_required
def foro_create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            # crear el primer post
            initial = form.cleaned_data.get('initial_post')
            if initial:
                Post.objects.create(thread=thread, author=request.user, content=initial)
            messages.success(request, 'Hilo creado correctamente')
            return redirect('foro_thread_detail', thread_id=thread.id)
    else:
        form = ThreadForm()
    return render(request, 'foro_create_thread.html', {'form': form})


@login_required
def foro_reply(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            # actualizar la fecha de actividad del hilo
            thread.updated_at = timezone.now()
            thread.save()
            messages.success(request, 'Respuesta publicada')
    return redirect('foro_thread_detail', thread_id=thread.id)

def documentos_index(request):
    """Vista para listar documentos con filtrado por etiquetas"""
    documentos = Document.objects.filter(activo=True)
    etiquetas = Tag.objects.all()
    etiquetas_seleccionadas = request.GET.getlist('tags')
    
    if etiquetas_seleccionadas:
        documentos = documentos.filter(etiquetas__id__in=etiquetas_seleccionadas).distinct()
    
    busqueda = request.GET.get('q')
    if busqueda:
        documentos = documentos.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    context = {
        'documentos': documentos,
        'etiquetas': etiquetas,
        'etiquetas_seleccionadas': [int(tag_id) for tag_id in etiquetas_seleccionadas],
        'busqueda': busqueda
    }
    return render(request, 'documentos_index.html', context)

def documento_detail(request, doc_id):
    """Vista para mostrar detalle de un documento"""
    documento = get_object_or_404(Document, id=doc_id, activo=True)
    return render(request, 'documento_detail.html', {'documento': documento})