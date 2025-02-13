from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from app.models import Usuario, Documento, Medidas, OrganismoSectorial


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'organismo_sectorial', 'autorizado_para_reportes')


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_medida', 'archivo', 'fecha_subida', 'estado')


class MedidaAdmin(admin.ModelAdmin):     #OJO AQUI
    list_display = ('nombre', 'extension_permitida')
    #'get_organismos_permitidos', 

    def get_organismos_permitidos(self, obj):
        return ", ".join([org.codigo_ente for org in obj.organismos_permitidos.all()])
    
    get_organismos_permitidos.short_description = "Organismos Permitidos"


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Medidas, MedidaAdmin)
admin.site.register(OrganismoSectorial)