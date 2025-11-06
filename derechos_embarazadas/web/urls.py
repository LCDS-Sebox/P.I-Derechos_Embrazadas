from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # URLs de documentos
    path('documentos/', views.documentos_index, name='documentos_index'),
    path('documentos/<int:doc_id>/', views.documento_detail, name='documento_detail'),
    path('caso/<int:caso_id>/', views.caso_detalle, name='caso_detalle'),
    path('categoria/<str:categoria>/', views.casos_por_categoria, name='casos_categoria'),
    # Foro
    path('foro/', views.foro_index, name='foro_index'),
    path('foro/new/', views.foro_create_thread, name='foro_create_thread'),
    path('foro/thread/<int:thread_id>/', views.foro_thread_detail, name='foro_thread_detail'),
    path('foro/thread/<int:thread_id>/reply/', views.foro_reply, name='foro_reply'),
]