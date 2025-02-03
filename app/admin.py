from django.contrib import admin

# Register your models here.

from app.models import Usuario, Documento, TipoDocumentoPermitido


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('codigo_ente', 'tipo_ente')


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_documento', 'archivo', 'fecha_subida', 'estado')


class TipoDocumentoPermitidoAdmin(admin.ModelAdmin):     #OJO AQUI
    list_display = ('get_entes_permitidos', 'nombre', 'extension_permitida')

    def get_entes_permitidos(self, obj):
        return ", ".join([ente.username for ente in obj.entes_permitidos.all()])
    
    get_entes_permitidos.short_description = "Entes Permitidos"  # Nombre de la columna en el admin


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(TipoDocumentoPermitido, TipoDocumentoPermitidoAdmin)