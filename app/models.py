from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint
from app.api.validators import custom_validate_file
from django.core.exceptions import ValidationError

# Create your models here.

class Usuario(AbstractUser):     #CLASE QUE HEREDA DE AbstractUser LA QUE PERMITE AGREGAR CAMPOS PERSONALIZADOS A USER
    """
    Modelo de Usuario personalizado que representa un organismo sectorial (fiscalizador).
    Hereda todas las funcionalidades básicas de usuario de Django y añade
    campos específicos para el ente fiscalizador.
    """

    #lista de tuplas: ('valor_en_database', 'nombre_legible')
    TIPOS_ENTE = [
        ('servicio_evaluacion_ambiental', 'Servicio de Evaluación Ambiental'),
        ('superintendencia_electricidad_combustibles', 'Superintendencia de Electricidad y Combustibles'),
        ('intendencia_regional_valparaiso', 'Intendencia Regional de Valparaíso'),
        ('dg_territorio_maritimo_y_marina_mercante', 'Dirección General de Territorio Marítimo y Marina Mercante'),
        ('corporacion_nacional_forestal', 'Corporación Nacional Forestal'),
        ('servicio_agricola_ganadero', 'Servicio Agrícola y Ganadero'),
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
        on_delete=models.CASCADE,
        # limit_choices_to=models.Q(tipo_ente=models.F('usuario__tipo_ente'))     #limit choices to filtra los tipo_documento que aparecen en el admin de Django para que solo muestre aquellos que coincidan con el tipo_ente del usuario
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

    def clean(self):     #metodo para validar datos de un formulario
        """ Valida que el usuario tenga permiso para subir este tipo de documento, osea que esté en la lista de entes_permitidos del documento """
        if not self.tipo_documento.entes_permitidos.filter(id=self.usuario.id).exists():
            raise ValidationError({'tipo_documento': "Este tipo de documento no está permitido para su usuario."})

    def save(self, *args, **kwargs):
        self.clean()  # Llamar a la validación antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.codigo_ente} - {self.tipo_documento.nombre}"
    


class TipoDocumentoPermitido(models.Model):     #define la configuracion del documento que puede subir cada ente fiscalizador. No confundir con extensión de documento
    """
    Se define qué tipos de documentos pueden subir cada ente fiscalizador.
    """

    TIPOS_DOCUMENTOS = [
        ('CIF', 'Catastro de incendios forestales'),
        ('IPC', 'Informe plan de comunicacion')
    ]    #AGREGAR MAS TIPOS DE DOCUMENTOS
    

    # tipo_ente = models.CharField(     #ente que lo puede subir
    #     max_length=50,
    #     choices=Usuario.TIPOS_ENTE,
    #     verbose_name='Tipo de ente fiscalizador'
    # )

    nombre = models.CharField(max_length=100)     #documento específico que puede subir cada organismo. Ejemplo: "Catastro de incendios forestales"
    descripcion = models.TextField(blank=True)
    extension_permitida = models.CharField(max_length=10)

    obligatorio = models.BooleanField(
        default=False,
        help_text="Indica si este documento es de entrega obligatoria"
    )

    #cada tipo de documento puede asociarse a multiples usuarios
    entes_permitidos = models.ManyToManyField(Usuario, related_name='documentos_permitidos')     #permite asociar varios usuarios a un mismo documento 
    

    class Meta:
        constraints = [
            UniqueConstraint(fields=['nombre'], name='unique_tipo_documento')     #UniqueConstraint impone restricciones de unicidad
            #en uno o mas campos de la base de datos evitando que se repitan En este caso, no peuden haber 2 tipos de documentos con el mismo nombre. 
            #Campo "nombre" debe ser unico en la tabla
        ]     

    def __str__(self):
        # Muestra los nombres de los entes permitidos en una lista
        entes = ", ".join([ente.username for ente in self.entes_permitidos.all()])
        return f"{self.nombre} - Permitido para: {entes}" if entes else f"{self.nombre}"

    #Para que esta clase funcione correctamente, primero debemos registrar en la base de datos los tipos de documentos permitidos. Ejemplo:

    # tipo_doc = TipoDocumentoPermitido.objects.create(
            #     tipo_ente='servicio_evaluacion_ambiental',
            #     nombre='Informe material particulado',
            #     descripcion='Informe detallado de emisiones de material particulado',
            #     extension_permitida='.pdf',
            #     obligatorio=True
    # )   

