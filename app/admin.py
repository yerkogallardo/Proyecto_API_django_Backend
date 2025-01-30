from django.contrib import admin

# Register your models here.

from app.models import Usuario, Documento, TipoDocumentoPermitido


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('codigo_ente', 'tipo_ente')


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_documento', 'archivo', 'fecha_subida', 'estado')


class TipoDocumentoPermitidoAdmin(admin.ModelAdmin):
    list_display = ('tipo_ente', 'nombre', 'extension_permitida')


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(TipoDocumentoPermitido, TipoDocumentoPermitidoAdmin)