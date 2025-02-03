from rest_framework import serializers
from app.models import Documento, TipoDocumentoPermitido

#Aquí validaremos la información entrante para garantizar seguridad e integridad

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        # fields = ['tipo_documento', 'archivo', 'fecha_subida', 'estado']
        # read_only_fields = ['estado']      #campo solo lectura
        fields = '__all__'



    # def validate_tipo_documento(self, value):
    #     tipos_validos = [tipo[0] for tipo in TipoDocumentoPermitido.TIPOS_DOCUMENTOS]
    #     if value.nombre not in tipos_validos:
    #         raise serializers.ValidationError("Tipo de documento no permitido.")
    #     return value
    #El parámetro value en la función validate_tipo_documento representa el valor del campo tipo_documento que se está validando cuando se envía una solicitud a la API.



    #verificamos que el tipo de documento corresponda al ente fiscalizador

    #antes de llegar a este metodo, se crea un diccionario "data" que representa un objeto creado previamente con los campos del modelo "TipoDocumentoPermitido"
    
    def validate(self, data):     #data corresponde a un diccionario que contiene todos los datos que llegan en la peticion despues de una validacion inicial previo a esta funcion validate()
        usuario = data['usuario']     #asigno la instancia actual del usuario. este tendrá sus atributos definidos
        tipo_doc = data['tipo_documento']     #data['tipo_documento'] va a contener todos los atributos y metodos, ya que mediante ForeignKey el campo tipo_documento de la clase Documento contiene TODOS los atributos de la clase TipoDocumentoPermitido. Se lee de la siguiente forma: <TipoDocumentoPermitido: id=1, tipo_ente= ... >

        # Verificar que el usuario tenga permitido subir este tipo de documento
        if not tipo_doc.entes_permitidos.filter(id=usuario.id).exists():
            raise serializers.ValidationError(
                {"tipo_documento": "Este tipo de documento no está permitido para su usuario."}
            )
        return data



        # if usuario.tipo_ente != tipo_doc.tipo_ente:     #si el tipo_ente presente en tipo_doc es diferente al tipo_ente de usuario:
        #     raise serializers.ValidationError(
        #         "Este tipo de documento no está permitido para su tipo de ente fiscalizador"
        #     )
        # return data     #si todo va bien, finaliza la validacion y devuelve datos validados. Luego se dirige a método create(self, calidated_data)
    



    def create(self, validated_data):     #crea el objeto en la base de datos con los datos ya validados
        #asigna automaticamente el usuario actual
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

    