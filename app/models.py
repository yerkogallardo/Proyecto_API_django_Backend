from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):     #CLASE QUE HEREDA DE AbstractUser LA QUE PERMITE AGREGAR CAMPOS PERSONALIZADOS A USER
    """
    Modelo de Usuario personalizado que representa un organismo sectorial (fiscalizador).
    Hereda todas las funcionalidades básicas de usuario de Django y añade
    campos específicos para el ente fiscalizador.
    """
    TIPOS_ENTE = [
        'servicio_evaluacion_ambiental,',
        'superintendencia_electricidad_combustibles',
        'intendencia_regional_valparaiso',
        'dg_territorio_maritimo_y_marina_mercante',    #dg = direccion general
        'corporacion_nacional_forestal',
        'servicio_agricola_ganadero'
    ]

    tipo_ente = models.CharField(
        max_length=100,
        choices = TIPOS_ENTE,
        verbose_name = 'Tipo de ente fiscalizador'
    )

    codigo_ente = models.CharField(
        max_length=20,
        unique = True,
        verbose_name = 'Código del ente'
    )

    region = models.CharField(
        max_length=100,
        verbose_name='Region',
        blank=True
    )

    class Meta:
        permissions = [
            ("can_upload_documents", "Puede subir documentos"),
            ("can_view_all_documents", "Puede ver todos los documentos"),
        ]

    def __str__(self):
        return f"{self.get_tipo_ente_display()} - {self.username}"     #Metodo especial creado por django automaticamente al definir un capo con "choices". Permite acceder al dato "amigable"
    


def documento_upload_path(instance, filename):
    #Generamos una ruta personalizada basada en el usuario (ente fiscalizador) y el tipo de documento
    return f"documentos/{instance.usuario.codigo_ente}/{instance.tipo_documento.nombre}/{filename}"



class Documento(models.Model):     #clase que representa cada archivo que se sube al sistema
    """
    Modelo para manejar los documentos subidos por los entes fiscalizadores.
    Cada documento está asociado directamente con el usuario que lo subió.
    """
    usuario = models.ForeignKey(     #usuario que sube el archivo
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='documentos'
        )
    
    tipo_documento = models.ForeignKey(     
        'TipoDocumentoPermitido',
        on_delete=models.CASCADE
    )

    archivo = models.FileField(     #que archivo es
        upload_to=documento_upload_path,
        validators=[custom_validate_file]     #Funcion validadora a crear. Corchetes ya que validators espera una lista de funciones validadoras (pueden ser varias)
    )

    fecha_subida=models.DateTimeField(auto_now_add=True)

    estado=models.CharField(
        max_length=20,
        choices=[
            ('PENDIENTE', 'Pendiente de revisión'),     ##########
            ('APROBADO', 'aprobado'),
            ('RECHAZADO', 'rechazado')
        ],
        default='PENDIENTE'
    )

    def __str__(self):
        return f"{self.usuario.codigo_ente} - {self.tipo_documento.nombre}"
    


class TipoDocumentoPermitido(models.Model):     #define que documento puede subir cada ente fiscalizador. 
    """
    Se define qué tipos de documentos pueden subir cada ente fiscalizador.
    """
    tipo_ente = models.CharField(
        max_length=50,
        choices=Usuario.TIPOS_ENTE,
        verbose_name='Tipo de ente fiscalizador'
    )

    nombre = models.CharField(max_length=100),
    descripcion = models.TextField(blank=True)
    extension_permitida = models.CharField(max_length=10)

    obligatorio = models.BooleanField(
        default=False,
        help_text="Indica si este documento es de entrega obligatoria"
    )
    
    class Meta:
        unique_together = ['tipo_ente', 'nombre']     ##########

    #Para que esta clase funcione correctamente, primero debemos registrar en la base de datos los tipos de documentos permitidos. Ejemplo:

    # tipo_doc = TipoDocumentoPermitido.objects.create(
            #     tipo_ente='servicio_evaluacion_ambiental',
            #     nombre='Informe material particulado',
            #     descripcion='Informe detallado de emisiones de material particulado',
            #     extension_permitida='.pdf',
            #     obligatorio=True
    # )   














# class Plan(models.Model):     #UN PLAN CONSIDERA UNA SERIE DE MEDIDAS

#     estado = [
#             ('ACTIVO', 'activo'),
#             ('PAUSADO', 'pausado'),
#             ('ATRASADO', 'atrasado'),
#             ('FINALIZADO', 'finalizado'),
#             ]
#     id_plan = models.AutoField(primary_key=True)
#     nombre_plan = models.CharField(max_length=255)
#     estado_avance = models.CharField(max_length=20, choices=estado, default='ACTIVO')
#     fecha_creación = models.DateTimeField(auto_now_add=True)
#     ultima_atcualizacion = models.DateField(auto_now=True)

#     def __str__(self):
#         return f'Nombre plan: {self.nombre_plan}. Estado actual: {self.estado_avance}'



# class MedidasDeAvance(models.Model):
#     tipo_medida = [
#                    ('AMBIENTAL', 'ambiental'),
#                    ('SECTORIAL', 'sectorial')
#                    ]
#     id_avance = models.AutoField(primary_key=True)
#     nombre_medida = models.CharField(max_length=75)
#     detalles = models.TextField(max_length=2000)
#     fecha_creación = models.DateTimeField(auto_now_add=True)
#     ultima_atcualizacion = models.DateField(auto_now=True)
#     id_plan = models.ForeignKey(Plan, on_delete=models.PROTECT)



# class Superintendencia(User):
#     id_tipo = models.AutoField(primary_key=True)
#     tipo_usuario = models.CharField(max_length=75, default='Superintendencia')



# class OrganismoSectorial(User):
    
#     lista_organismos = [
#         'servicio_evaluacion_ambiental,',
#         'superintendencia_electricidad_combustibles',
#         'intendencia_regional_valparaiso',
#         'dg_territorio_maritimo_y_marina_mercante',    #dg = direccion general
#         'corporacion_nacional_forestal',
#         'servicio_agricola_ganadero'
#     ]

#     localidades = [
#         'Quintero', 'Concon', 'Puchuncavi'
#     ]

#     id_tipo = models.AutoField(primary_key=True)
#     organismo = models.CharField(max_length=255, choices=lista_organismos)
#     empresa_fiscalizada = models.CharField(max_length=75)
#     localidad = models.CharField(max_length=75, choices=localidades)
#     observaciones = models.TextField(max_length=500)
#     rca_aprobadas = models.FileField()    #CAMPO PARA AGREGAR ARCHIVOS
#     fecha_creación = models.DateTimeField(auto_now_add=True)
#     ultima_atcualizacion = models.DateField(auto_now=True)


#     def documentos_por_organismo(self):    #LOGICA PARA FILTRAR LOS DOCUMENTOS A SUBIR POR TIPO ORGANISMO
        




