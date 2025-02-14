from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from app.models import Usuario, Reporte, Medidas, OrganismoSectorial


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'organismo_sectorial', 'autorizado_para_reportes')



class OrganismoSectorialAdmin(admin.ModelAdmin):
    list_display = ('codigo_ente', 'tipo_ente', 'region')



class MedidaAdmin(admin.ModelAdmin):     #OJO AQUI
    list_display = ('nombre', 'descripcion', 'extension_permitida', 'obligatorio')
    #'get_organismos_permitidos', 

    def get_organismos_permitidos(self, obj):
        return ", ".join([org.codigo_ente for org in obj.organismos_permitidos.all()])
    
    get_organismos_permitidos.short_description = "Organismos Permitidos"



class ReporteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_medida', 'archivo', 'fecha_subida', 'estado')



admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(OrganismoSectorial, OrganismoSectorialAdmin)
admin.site.register(Medidas, MedidaAdmin)
admin.site.register(Reporte, ReporteAdmin)

