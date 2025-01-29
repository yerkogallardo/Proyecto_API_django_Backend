from rest_framework import serializers
from app.models import Documento

#Aquí validaremos la información entrante para garantizar seguridad e integridad

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = ['tipo_documento', 'archivo', 'fecha_subida', 'estado']
        read_only_fields = ['estado']      #campo solo lectura
    

    #verificamos que el tipo de documento corresponda al ente fiscalizador

    #antes de llegar a este metodo, se crea un diccionario "data" que representa un objeto creado previamente con los campos del modelo "TipoDocumentoPermitido"
    
    def validate(self, data):     #data corresponde a un diccionario que contiene todos los datos que llegan en la peticion despues de una validacion inicial previo a  validate()
        usuario = self.context['request'].user     #asigno la instancia actual del usuario
        tipo_doc = data['tipo_documento']     #data['tipo_documento'] va a contener todos los atributos y metodos, ya que mediante ForeignKey el campo tipo_documento de la clase Documento contiene TODOS los atributos de la clase TipoDocumentoPermitido. Se lee de la siguiente forma: <TipoDocumentoPermitido: id=1, tipo_ente= ... >

        if tipo_doc.tipo_ente != usuario.tipo_ente:     #si el tipo_ente presente en tipo_doc es diferente al tipo_ente de usuario:
            raise serializers.ValidationError(
                "Este tipo de documento no está permitido para su tipo de ente fiscalizador"
            )
        return data     #si todo va bien, finaliza la validacion y devuelve datos validados. Luego se dirige a método create(self, calidated_data)
    

    def create(self, validated_data):     #crea el objeto en la base de datos con los datos ya validados
        #asigna automaticamente el usuario actual
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

    