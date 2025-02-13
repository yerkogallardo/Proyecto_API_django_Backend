from rest_framework import serializers
from app.models import Reporte, Medidas, OrganismoSectorial

#Aquí validaremos la información entrante para garantizar seguridad e integridad

class MedidasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medidas
        fields = '__all__'


class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'

    """verificamos que la Medida corresponda al ente fiscalizador
    antes de llegar a este metodo, se crea un diccionario "data" que representa 
    un objeto creado previamente con los campos del modelo Medidas"""
    
    def validate(self, data):     #data corresponde a un diccionario que contiene todos los datos que llegan en la peticion despues de una validacion inicial previo a esta funcion validate()
        usuario = data['usuario']     #asigno la instancia actual del usuario. este tendrá sus atributos definidos
        tipo_doc = data['tipo_medida']     #data['tipo_medida'] va a contener todos los atributos y metodos, ya que mediante ForeignKey el campo tipo_medida de la clase Reporte contiene TODOS los atributos de la clase Medidas. Se lee de la siguiente forma: <Medidas: id=1, tipo_ente= ... >

        # Verificar que el usuario tenga permitido subir este tipo de documento
        if not tipo_doc.organismos_permitidos.filter(id=usuario.id).exists():
            raise serializers.ValidationError(
                {"medida": "Esta medida no está permitida para su usuario."}
            )
        return data



    def create(self, validated_data):     
        """crea el objeto en la base de datos con los datos ya validados
        asigna automaticamente el usuario actual"""
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)



    
class OrganismoSectorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoSectorial
        fields = '__all__'