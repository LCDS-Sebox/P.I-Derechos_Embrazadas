from django.db import models
from django.core.validators import FileExtensionValidator

class Tag(models.Model):
    """Modelo para etiquetas de documentos"""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#e91e63", help_text="Color en formato HEX (ej: #FF0000)")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ['nombre']

class Document(models.Model):
    """Modelo para documentos PDF"""
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    archivo = models.FileField(
        upload_to='documentos/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    etiquetas = models.ManyToManyField(Tag, related_name='documentos')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ['-fecha_subida']

class CasoProblema(models.Model):
    """Modelo para casos de problemas con derechos de embarazadas"""
    
    CATEGORIAS = [
        ('legal', 'Protección Legal'),
        ('medica', 'Atención Médica'),
        ('laboral', 'Derechos Laborales'),
        ('licencias', 'Licencias Maternales'),
    ]
    
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    icono = models.CharField(max_length=10, default='⚖️')
    descripcion_corta = models.TextField(max_length=200)
    descripcion_completa = models.TextField()
    que_hacer = models.TextField(help_text="Qué hacer en esta situación")
    donde_acudir = models.TextField(help_text="Dónde acudir por ayuda")
    leyes_aplicables = models.TextField(blank=True, help_text="Leyes que respaldan este derecho")
    ejemplos = models.TextField(blank=True, help_text="Ejemplos de casos reales")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Caso de Problema'
        verbose_name_plural = 'Casos de Problemas'
        ordering = ['categoria', 'titulo']
    
    def __str__(self):
        return f"{self.titulo} ({self.get_categoria_display()})"


class Thread(models.Model):
    """Hilo del foro"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='threads'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    locked = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class Post(models.Model):
    """Respuesta dentro de un hilo"""
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Post by {self.author} on {self.thread}"