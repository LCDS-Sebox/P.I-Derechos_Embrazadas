from django.contrib import admin
from .models import CasoProblema, Thread, Post, Document, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'color')
    search_fields = ('nombre', 'descripcion')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_subida', 'activo', 'get_etiquetas')
    list_filter = ('activo', 'etiquetas', 'fecha_subida')
    search_fields = ('titulo', 'descripcion')
    filter_horizontal = ('etiquetas',)
    
    def get_etiquetas(self, obj):
        return ", ".join([tag.nombre for tag in obj.etiquetas.all()])
    get_etiquetas.short_description = 'Etiquetas'

@admin.register(CasoProblema)
class CasoProblemaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'activo', 'fecha_creacion')
    list_filter = ('categoria', 'activo', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion_corta', 'descripcion_completa')
    list_editable = ('activo',)
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'categoria', 'icono', 'descripcion_corta')
        }),
        ('Contenido Detallado', {
            'fields': ('descripcion_completa', 'que_hacer', 'donde_acudir')
        }),
        ('Información Adicional', {
            'fields': ('leyes_aplicables', 'ejemplos'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        )


    @admin.register(Thread)
    class ThreadAdmin(admin.ModelAdmin):
        list_display = ('title', 'author', 'created_at', 'updated_at', 'locked')
        list_filter = ('locked', 'created_at')
        search_fields = ('title',)


    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_display = ('thread', 'author', 'created_at')
        search_fields = ('content',)